#!/usr/bin/env python3
"""Run JSON Schema evaluation fixtures against Draft 2020-12."""
import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"
CASES_FILE = ASSETS / "evaluation-cases.json"
OUTPUT_SCHEMA_FILE = ASSETS / "official-metaschemas" / "output-schema.json"

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry
    from referencing.jsonschema import DRAFT202012
    from referencing.exceptions import Unresolvable
except ImportError:
    print(
        "Missing dependencies: install with "
        "python3 -m pip install jsonschema referencing",
        file=sys.stderr,
    )
    sys.exit(2)


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_registry(case):
    resources = []
    for rel in case.get("registry", []):
        schema_path = ASSETS / rel
        schema = load_json(schema_path)
        uri = schema.get("$id")
        if not uri:
            raise ValueError(f"Registry schema {rel} is missing $id")
        resources.append((uri, DRAFT202012.create_resource(schema)))
    if "schema_file" in case:
        schema_path = ASSETS / case["schema_file"]
        schema = load_json(schema_path)
        uri = schema.get("$id")
        if uri and all(uri != u for u, _ in resources):
            resources.append((uri, DRAFT202012.create_resource(schema)))
    for rel in ["examples/tree-base.schema.json", "examples/tree-strict.schema.json"]:
        schema = load_json(ASSETS / rel)
        uri = schema["$id"]
        if all(uri != u for u, _ in resources):
            resources.append((uri, DRAFT202012.create_resource(schema)))
    return Registry().with_resources(resources)


def resolve_schema(case):
    if "schema" in case:
        return case["schema"]
    if "schema_file" in case:
        return load_json(ASSETS / case["schema_file"])
    raise ValueError(f"Case {case.get('id')} has neither schema nor schema_file")


def check_schema(schema):
    Draft202012Validator.check_schema(schema)


def error_matches(error, expected):
    if "validator" in expected and error.validator != expected["validator"]:
        return False
    if "instancePath" in expected and list(error.absolute_path) != expected["instancePath"]:
        return False
    return True


def run_validation_case(case, format_assertion=False):
    schema = resolve_schema(case)
    try:
        check_schema(schema)
    except Exception as exc:
        return [f"  SCHEMA-INVALID {case['id']}: {exc}"]
    registry = build_registry(case)
    kwargs = {"registry": registry}
    if format_assertion or case.get("kind") == "format-assertion":
        kwargs["format_checker"] = Draft202012Validator.FORMAT_CHECKER
    validator = Draft202012Validator(schema, **kwargs)
    failures = []
    for test in case["tests"]:
        if case.get("kind") == "unresolved-ref":
            try:
                validator.is_valid(test["instance"])
            except Exception:
                continue
            failures.append(
                f"  FAIL {test['description']}: expected reference resolution error"
            )
            continue
        try:
            result = validator.is_valid(test["instance"])
        except Exception as exc:
            failures.append(f"  ERROR {test['description']}: {exc}")
            continue
        if result != test["valid"]:
            failures.append(
                f"  FAIL {test['description']}: expected valid={test['valid']} "
                f"got valid={result} for instance={test['instance']!r}"
            )
            continue
        expected = test.get("expected")
        if expected and not test["valid"]:
            errors = list(validator.iter_errors(test["instance"]))
            if not any(error_matches(e, expected) for e in errors):
                seen = [(e.validator, list(e.absolute_path)) for e in errors]
                failures.append(
                    f"  FAIL {test['description']}: expected error {expected} "
                    f"not found in {seen}"
                )
    return failures


def run_schema_invalid_case(case):
    failures = []
    for entry in case["schemas"]:
        try:
            check_schema(entry["schema"])
        except Exception:
            continue
        failures.append(
            f"  FAIL {entry['description']}: expected schema validation failure"
        )
    return failures


def run_output_conformance_case(case):
    output_schema = load_json(OUTPUT_SCHEMA_FILE)
    try:
        check_schema(output_schema)
    except Exception as exc:
        return [f"  OUTPUT-SCHEMA-INVALID: {exc}"]
    validator = Draft202012Validator(output_schema)
    failures = []
    for sample in case["samples"]:
        if not validator.is_valid(sample["output"]):
            errors = [e.message for e in validator.iter_errors(sample["output"])]
            failures.append(
                f"  FAIL {sample['description']}: output invalid: {errors}"
            )
    return failures


def run_case(case):
    kind = case.get("kind", "validation")
    if kind in ("validation", "format-assertion"):
        return run_validation_case(case)
    if kind == "schema-invalid":
        return run_schema_invalid_case(case)
    if kind == "unresolved-ref":
        return run_validation_case(case)
    if kind == "output-conformance":
        return run_output_conformance_case(case)
    return [f"  ERROR {case['id']}: unknown kind {kind!r}"]


def main():
    parser = argparse.ArgumentParser(description="Run JSON Schema example fixtures")
    parser.add_argument("--all", action="store_true", help="Run all cases")
    parser.add_argument("--example", help="Run one case by id")
    parser.add_argument("--list", action="store_true", help="List case ids")
    args = parser.parse_args()

    cases = load_json(CASES_FILE)["cases"]
    if args.list:
        for case in cases:
            print(f"{case['id']}: {case['description']}")
        return 0
    selected = cases
    if args.example:
        selected = [c for c in cases if c["id"] == args.example]
        if not selected:
            print(f"Unknown example: {args.example}", file=sys.stderr)
            return 2
    elif not args.all and not args.example:
        parser.print_help()
        return 2

    total_failures = []
    for case in selected:
        try:
            failures = run_case(case)
        except Exception as exc:
            failures = [f"  ERROR {case['id']}: {exc}"]
        unit = len(case.get("tests", case.get("schemas", case.get("samples", []))))
        status = "PASS" if not failures else "FAIL"
        print(f"{status} {case['id']} ({unit} checks)")
        total_failures.extend([f"[{case['id']}] {f}" for f in failures])
        for failure in failures:
            print(failure)
    if total_failures:
        print(f"\n{len(total_failures)} failing assertion(s)", file=sys.stderr)
        return 1
    print(f"\nAll {len(selected)} case(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
