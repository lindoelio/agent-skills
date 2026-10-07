---
name: json-schema
description: |
  Author, review, debug, migrate, and explain JSON Schema
  with verifiable Draft 2020-12 correctness. Use this skill
  whenever someone writes or validates a JSON Schema, debugs
  validation errors, composes schemas with
  allOf/anyOf/oneOf/not/if-then-else, structures schemas
  with $ref/$defs/$anchor, constrains
  objects/arrays/strings/numbers, uses
  unevaluatedProperties/unevaluatedItems, handles
  format/content annotations, declares $schema dialects and
  vocabularies, migrates from draft-04/06/07/2019-09, or
  asks about JSON Schema keywords, behavior, or best
  practices — even if they only say "schema",
  "validate JSON", or "API contract".
license: MIT
compatibility: JSON Schema Draft 2020-12; Python 3.9+ with
  jsonschema and referencing for scripts
metadata:
  author: agent-skills
  version: "1.0"
---

# JSON Schema

Write and evaluate JSON Schema from the released specification, not from memory.

## Gotchas

- `properties` neither requires presence nor implies `type: object`. Pair with
  `required` and `type` explicitly.
- Missing property and explicit `null` are different. `required` fails only on
  missing; `type` fails on `null` unless allowed.
- `default` never fills values during validation. It is an annotation only.
- `format` is annotation-only under the default 2020-12 dialect. Do not reject
  instances for bad `format` unless format-assertion is declared and supported.
- `contentEncoding`, `contentMediaType`, and `contentSchema` do not validate
  decoded content by default.
- `allOf` is intersection, not merging or inheritance. `additionalProperties`
  sees only the same subschema.
- `additionalProperties` and `unevaluatedProperties` are not interchangeable.
  The same holds for `items` and `unevaluatedItems`.
- `prefixItems` does not limit array length by itself. Add `items: false`,
  `minItems`, or `maxItems` when closure matters.
- Sibling keywords next to `$ref` apply in 2020-12. In draft-04 through draft-07
  they were ignored.
- `$id` is an identifier, not proof the schema is downloadable. Preload
  resources instead of assuming HTTP retrieval.
- `readOnly`, `writeOnly`, `title`, `description`, `examples`, and `$comment`
  never change validity.
- Unknown keywords SHOULD be treated as annotations, not errors. Missing
  keywords never fail.
- Never claim validation ran unless a validator actually ran.

## Quick Start

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "Product",
  "type": "object",
  "properties": {
    "productId": { "type": "integer" },
    "productName": { "type": "string", "minLength": 1 },
    "price": { "type": "number", "exclusiveMinimum": 0 }
  },
  "required": ["productId", "productName", "price"],
  "additionalProperties": false
}
```

```bash
cd json-schema && python3 scripts/run_examples.py --example product-closed
```

From the repository root, use `python3 json-schema/scripts/run_examples.py
--example product-closed`.

Valid `{"productId":1,"productName":"Door","price":12.5}` passes.
Missing `price`, zero `price`, or an extra property fails for a different stated
reason.

## Workflow

1. Identify context: task, dialect, implementation, and whether schemas or
instances are untrusted.
2. Preserve the existing `$schema` dialect. For new unconstrained work default
to 2020-12 and say so.
3. Load only the references needed for the task; see Reference Routing.
4. Translate each requirement into an explicit keyword decision. Record what is
intentionally left open.
5. Author or diagnose the smallest schema change that satisfies the requirement.
6. Validate schema syntax, resolve every `$ref` and `$dynamicRef`, then test
positive, negative, boundary, missing/null, and wrong-type cases.
7. Report validity, evidence, dialect, limitations, and any source conflict. Do
not invent validator behavior.

## Source Authority

Released specification text governs semantics. Meta-schemas describe syntax
only.
Guides explain. Library documentation describes one implementation.

Read [sources-and-authority](references/sources-and-authority.md) before citing
behavior,
changing dialects, or resolving a documentation conflict.

Cite consequential claims with the specification section, for example
`Core Sec. 10.2.1.1 allOf` or `Validation Sec. 6.1.1 type`.
Preserve RFC 2119 strength: do not turn `SHOULD` into `MUST`.

## Reference Routing

- Keyword lookup, vocabulary, value shape:
  [keyword-index](references/keyword-index.md)
- Type, numeric, string, enum/const rules:
  [validation](references/validation.md)
- Objects, arrays, tuples, containment:
  [objects-and-arrays](references/objects-and-arrays.md)
- Boolean logic, conditionals, evaluation:
  [composition-and-evaluation](references/composition-and-evaluation.md)
- `$ref`, `$defs`, anchors, JSON Pointer, bundling:
  [references-and-bundling](references/references-and-bundling.md)
- `$dynamicRef`, `$dynamicAnchor`, recursion:
  [dynamic-references](references/dynamic-references.md)
- `$schema`, meta-schemas, vocabularies, custom keywords:
  [dialects-and-vocabularies](references/dialects-and-vocabularies.md)
- `format`, `content*`: [formats-and-content](references/formats-and-content.md)
- Metadata, `$comment`, output formats:
  [annotations-and-output](references/annotations-and-output.md)
- Draft migration and breaking changes: [migration](references/migration.md)
- Tooling, untrusted input, unsupported rules:
  [tooling-security-and-limits](references/tooling-security-and-limits.md)

Load `sources-and-authority.md` plus at most two task references by default.
Load migration whenever `$schema` is absent, legacy, mixed, or being changed.

## Verification

Use an established validator, never a homemade validation engine.

```bash
cd json-schema && python3 scripts/run_examples.py --all
cd json-schema && python3 scripts/check_skill.py
```

From the repository root, prefix both commands with `json-schema/`, for example
`python3 json-schema/scripts/run_examples.py --all`.

Rules:

- Validate schemas separately from instances.
- Preload local resources. Disable automatic network retrieval.
- Cover valid, invalid, boundary, missing versus `null`, and wrong-type cases.
- Label implementation-specific `format` assertion or annotation collection
  separately.
- Treat unsupported requirements as explicit limitations, not passing tests.

Assets live in `assets/`: pinned `source-manifest.json`, machine-readable
`keyword-registry.json`, vendored 2020-12 meta-schemas, runnable `examples/`,
and `evaluation-cases.json` regression fixtures.

## Output Shape

For every task report dialect, validity, evidence, and limits:

```markdown
Dialect: 2020-12, assumed|declared
Result: valid|invalid|not run, with command and validator version
Failing keyword: keyword and instance location, or none
Evidence: schema check, instance cases, source sections
Limits: unresolved refs, format behavior, unsupported requirements
```
