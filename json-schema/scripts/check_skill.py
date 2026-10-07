#!/usr/bin/env python3
"""Structural checks for the json-schema skill."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
REF_DIR = ROOT / "references"
ASSETS = ROOT / "assets"

errors = []


def fail(message):
    errors.append(message)


def folded_description(front):
    match = re.search(r"description:\s*\|(.*)(?=\n\w+:)", front, re.DOTALL)
    if not match:
        return None
    lines = match.group(1).splitlines()
    stripped = [line.strip() for line in lines if line.strip()]
    return " ".join(stripped)


def check_frontmatter():
    text = SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
        return
    end = text.find("\n---\n", 4)
    if end < 0:
        fail("SKILL.md frontmatter is not closed")
        return
    front = text[4:end]
    for key in ["name:", "description:", "license:", "compatibility:", "metadata:"]:
        if key not in front:
            fail(f"SKILL.md frontmatter missing {key}")
    match = re.search(r"^name:\s*(\S+)", front, re.MULTILINE)
    if not match or match.group(1) != "json-schema":
        fail("SKILL.md name must be exactly json-schema")
    desc = folded_description(front)
    if desc is None:
        fail("SKILL.md description block not found")
    elif len(desc) > 1024:
        fail(f"description is {len(desc)} characters, limit is 1024")
    lines = text.splitlines()
    if len(lines) > 500:
        fail(f"SKILL.md has {len(lines)} lines, keep under 500")


def check_references():
    expected = [
        "sources-and-authority.md",
        "keyword-index.md",
        "validation.md",
        "objects-and-arrays.md",
        "composition-and-evaluation.md",
        "references-and-bundling.md",
        "dynamic-references.md",
        "dialects-and-vocabularies.md",
        "formats-and-content.md",
        "annotations-and-output.md",
        "migration.md",
        "tooling-security-and-limits.md",
    ]
    for name in expected:
        path = REF_DIR / name
        if not path.exists():
            fail(f"missing references/{name}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 1000:
            fail(f"references/{name} exceeds 1000 lines")
        if not lines or not lines[0].startswith("# "):
            fail(f"references/{name} must start with an H1")
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    for name in expected:
        if name not in skill_text:
            fail(f"SKILL.md does not route to references/{name}")


def check_registry():
    registry = json.loads((ASSETS / "keyword-registry.json").read_text(encoding="utf-8"))
    keywords = registry.get("keywords", [])
    names = [k["name"] for k in keywords]
    if len(names) != 57:
        fail(f"keyword registry has {len(names)} keywords, expected 57")
    for required in ["$ref", "$dynamicRef", "prefixItems", "unevaluatedProperties", "dependentRequired", "contentSchema"]:
        if required not in names:
            fail(f"keyword registry missing {required}")
    formats = registry.get("formats", [])
    if len(formats) != 19:
        fail(f"keyword registry has {len(formats)} formats, expected 19")
    for required in ["date-time", "uri-reference", "relative-json-pointer", "regex"]:
        if required not in formats:
            fail(f"keyword registry missing format {required}")


def sha256_of(path):
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def check_assets():
    for name in ["source-manifest.json", "keyword-registry.json", "evaluation-cases.json", "THIRD-PARTY-NOTICES.md"]:
        if not (ASSETS / name).exists():
            fail(f"missing assets/{name}")
    metas = list((ASSETS / "official-metaschemas").glob("*.json"))
    if len(metas) < 10:
        fail(f"expected at least 10 vendored meta-schemas, found {len(metas)}")
    for path in metas:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"invalid JSON in {path.name}: {exc}")
    examples = list((ASSETS / "examples").glob("*.schema.json"))
    if len(examples) < 5:
        fail(f"expected at least 5 examples, found {len(examples)}")
    try:
        cases = json.loads((ASSETS / "evaluation-cases.json").read_text(encoding="utf-8"))["cases"]
        if len(cases) < 10:
            fail(f"expected at least 10 evaluation cases, found {len(cases)}")
    except Exception as exc:
        fail(f"invalid evaluation-cases.json: {exc}")
    try:
        manifest = json.loads((ASSETS / "source-manifest.json").read_text(encoding="utf-8"))
        for entry in manifest.get("vendored_metaschemas", []):
            actual = sha256_of(ASSETS / entry["path"])
            if actual != entry["sha256"]:
                fail(f"digest mismatch for {entry['path']}")
        for entry in manifest.get("pinned_assets", []):
            actual = sha256_of(ASSETS / entry["path"])
            if actual != entry["sha256"]:
                fail(f"digest mismatch for {entry['path']}")
    except Exception as exc:
        fail(f"invalid source-manifest.json: {exc}")


def check_dependencies():
    try:
        manifest = json.loads((ASSETS / "source-manifest.json").read_text(encoding="utf-8"))
        tested = {d["package"]: d["version"] for d in manifest.get("dependencies", {}).get("tested", [])}
        from importlib.metadata import version

        for package, expected in tested.items():
            try:
                installed = version(package)
            except Exception:
                fail(f"dependency {package} is not installed")
                continue
            print(f"validator: {package} {installed} (pinned {expected})")
            if installed != expected:
                fail(f"dependency {package} is {installed}, pinned {expected}")
    except Exception as exc:
        fail(f"dependency check failed: {exc}")


def main():
    if not SKILL_MD.exists():
        print("missing json-schema/SKILL.md", file=sys.stderr)
        return 1
    check_frontmatter()
    check_references()
    check_registry()
    check_assets()
    check_dependencies()
    if errors:
        print("check_skill FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("check_skill passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
