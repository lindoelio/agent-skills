# Migration

Use this reference whenever `$schema` is absent, legacy, mixed, or being
changed.

## Preserve or declare explicitly

Do not silently upgrade old schemas. Preserve the existing dialect unless
migration
is requested. When migrating, change `$schema`, update breaking keywords, and
retest
every affected behavior. Mechanical renaming is not enough.

## 2020-12 breaking and high-risk changes

- Array tuple syntax changed from array-form `items` to `prefixItems`.
- Extra array items changed from `additionalItems` to schema-form `items`.
- `$recursiveRef` became `$dynamicRef` with a named fragment.
- `$recursiveAnchor` became a named `$dynamicAnchor`.
- `contains` matches now count as evaluated for `unevaluatedItems`.
- Regular expressions are expected to support Unicode.
- The old `application/schema+json` media-type `schema` parameter was removed.
- Compound documents and bundling have explicit processing rules.
- `format` has separate annotation and assertion vocabularies.
- Unevaluated keywords moved into their own vocabulary.

Example tuple migration:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "array",
  "prefixItems": [{ "type": "number" }, { "type": "string" }],
  "items": false,
  "minItems": 2,
  "maxItems": 2
}
```

The pre-2020-12 equivalent used array-form `items` plus `additionalItems:
false`.

## 2019-09 changes

- `format` became annotation-only by default.
- Plain-name fragments moved from `$id` to `$anchor`.
- `$id` must not contain a non-empty fragment.
- `definitions` was renamed to `$defs`.
- `dependencies` split into `dependentRequired` and `dependentSchemas`.
- Added `unevaluatedItems`, `unevaluatedProperties`, `minContains`,
  `maxContains`, `deprecated`, `contentSchema`, `uuid`, and `duration`.
- Introduced vocabularies and standardized output formats.
- `$ref` siblings began applying alongside the reference.

The default meta-schema retains obsolete `definitions` and `dependencies`
transition names,
but new schemas should use `$defs`, `dependentRequired`, and `dependentSchemas`.

## Draft-06 changes

- Added `propertyNames`, `contains`, `const`, and `examples`.
- Added `uri-reference`, `uri-template`, and `json-pointer` formats.
- Replaced `id` with `$id` and made boolean schemas generally available.
- Changed boolean `exclusiveMinimum`/`exclusiveMaximum` to numeric bounds.
- Defined `1.0` as an integer under the broader draft-06 treatment.

## Draft-07 changes

- Added `if`, `then`, `else`, `$comment`, `readOnly`, `writeOnly`,
  `contentMediaType`, and `contentEncoding`.
- Added internationalized formats including `iri`, `iri-reference`, `idn-email`,
  `idn-hostname`, `relative-json-pointer`, `date`, `time`, and restored `regex`.
- Clarified annotation collection and `json-pointer` string encoding.
- Remains broadly backward compatible with draft-06 validation outcomes.

## Draft-06 and draft-04 traps

- `id` became `$id`. Old `id` is not equivalent in current documents.
- Boolean `exclusiveMinimum` and `exclusiveMaximum` became numeric bounds.
- `$ref` could appear only where a schema was expected; siblings were ignored.
- `$id` in a subschema was only a base-URI change before 2019-09, not an
  embedded resource.
- `1.0` counts as an integer in draft-06 onward, unlike the narrower draft-04
  treatment.
- Draft-05 has no separate meta-schema. It continues to use draft-04
  identifiers.
- There is no `regular expressions` type. That guide wording is wrong.
- `not` takes one schema. Do not migrate it as an array.
- Mixed-dialect bundles require per-resource `$schema` handling.

## Migration checklist

- Record the starting dialect and target dialect.
- Replace removed or renamed keywords with behavior-equivalent constructs.
- Update `$ref` sibling assumptions.
- Re-evaluate tuple, closure, containment, conditional, and dynamic-reference
  behavior.
- Validate every schema resource against its own meta-schema.
- Rerun positive, negative, boundary, missing/null, wrong-type, and reference
  tests.
- State remaining incompatibilities explicitly.
