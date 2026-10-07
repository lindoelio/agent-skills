# Annotations and Output

Use this reference for metadata, comments, annotation collection, and validation
output.

## Metadata annotations

```json
{
  "title": "Product",
  "description": "A product in the catalog",
  "default": "Untitled",
  "examples": ["Door", "Window"],
  "deprecated": false,
  "readOnly": false,
  "writeOnly": false
}
```

Rules:

- `title` and `description` are strings for documentation and UI display.
- `default` and `examples` should be consistent with the schema, but validity
  does not require it.
- Missing values are not filled from `default` during validation.
- `examples` values are flattened when multiple occurrences apply.
- `deprecated: true` discourages use but does not invalidate.
- `readOnly: true` means the owner manages the value. `writeOnly: true` means
  retrieval omits it, such as a password.
- Neither `readOnly` nor `writeOnly` enforces authorization.
- Multiple `readOnly`, `writeOnly`, or `deprecated` occurrences resolve toward
  `true` when any applicable occurrence is `true`.

## Comments

```json
{
  "$comment": "TODO: enumerate supported countries",
  "type": "object"
}
```

`$comment` is for schema maintainers only. Its value must be a string.
Implementations must not show it to end users, collect it as an annotation,
or act on its contents. It may be stripped during processing.

## Annotation collection

Collected annotations should include keyword name, instance location, schema
location path, absolute schema location when available, and attached values.

Important interactions:

- Failed schema locations do not contribute annotations.
- `not` and failing conditional branches suppress their enclosed annotations.
- `if` annotations may still be collected even when neither `then` nor `else`
  applies.
- Applicators aggregate annotations from applied subschemas and references.
- Unknown keywords SHOULD be collected as annotations with their values in
  verbose output contexts.

Short-circuit evaluation is appropriate for boolean-only checks, but complete
annotation collection may require evaluating branches that cannot change
validity.

## Output formats

Support flag, basic, or detailed output at minimum where available. Verbose
output
is optional. Support for detailed or verbose implies support for flag.

Every non-flag output unit should contain:

- `keywordLocation`: relative validation path, including `$ref` or
  `$dynamicRef`.
- `absoluteKeywordLocation`: canonical resource URI plus pointer where
  available.
- `instanceLocation`: JSON Pointer to the evaluated value.
- `error` for failures or `annotation` for successes.
- `errors` or `annotations` for nested results.

The official minimum-output schema is vendored as
`assets/official-metaschemas/output-schema.json`.

## Known output ambiguity

There is a documented ambiguity around `additionalProperties` output when
annotations
are optimized rather than collected directly. Validation results agree, but
detailed
output structure may differ by implementation.

Cite the ADR in `assets/source-manifest.json` when this matters, use validation
results rather than output shape for conformance, and do not assume one verbose
representation is universal.
