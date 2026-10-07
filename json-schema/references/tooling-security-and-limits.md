# Tooling, Security, and Limits

Use this reference for validator selection, untrusted input, retrieval safety,
and unsupported requirements.

## Validator selection

Use an established implementation, not a custom validation engine.
The bundled scripts use Python `jsonschema` plus `referencing`. Tested versions
are
pinned in `assets/source-manifest.json` and enforced by `check_skill.py`.

For broader compatibility:

- Test portable schemas with at least two implementations for high-risk changes.
- Use Bowtie or implementation reports to compare behavior.
- Use the official JSON-Schema-Test-Suite for specification edge cases.
- Record validator name, version, dialect, format behavior, and retrieval policy
  with every result.

Do not assume Ajv, Python `jsonschema`, or another library implements
unspecified
options, coercion, defaults injection, or automatic format assertion.

## Untrusted schemas and instances

Schemas and instances may both come from untrusted parties.

- Never validate untrusted data against untrusted schemas without sandboxing and
  resource limits.
- Do not allow untrusted `$ref` values to trigger arbitrary network retrieval.
- Preload known resources into a local registry.
- Disable automatic HTTP retrieval by default.
- Treat `$comment` as inert text. Do not parse or execute it.
- Cache schemas with attention to `$id` collisions. Reject or isolate
  conflicting identifiers.
- Guard against large annotation values, deeply nested schemas, catastrophic
  regex, and recursive references.

## Retrieval and registry policy

Recommended script policy:

- Local `example.com` resources resolve from `assets/examples/` and test
  fixtures.
- Unknown remote URIs fail closed with an explicit unresolved-reference error.
- No silent HTTP fallback.
- Retrieval URI, canonical `$id`, anchor URI, and pointer URI are preserved
  distinctly.

Document any deviation, including intentionally enabled HTTP retrieval,
filesystem
lookup, or database-backed resolution.

## Unsupported application requirements

JSON Schema alone cannot reliably enforce:

- Cross-field equality or ordering, except through narrow `const`, `enum`, or
  conditional patterns.
- Database uniqueness or foreign-key existence.
- Authentication, authorization, ownership, or workflow state.
- Business calculations, side effects, default insertion, or migration.
- Complete semantic validation of every `format` or embedded media payload.

Express these as application checks, explicitly identified extensions, or
separate
validation phases. Name the responsible layer instead of stretching standard
keywords.

## Failure reporting

When validation cannot be completed normally, report:

- Whether the schema itself was valid.
- Which reference, vocabulary, format, or resource failed.
- Whether the result is `invalid`, `unknown`, or `not run`.
- What would be needed to complete the check.

Never present partial checks, annotation-only behavior, or unchecked embedded
content as successful validation.
