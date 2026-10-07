# References and Bundling

Use this reference for `$ref`, `$defs`, anchors, JSON Pointer, URI handling, and
bundled documents.

## Reuse locations

```json
{
  "$id": "https://example.com/schemas/customer",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "first_name": { "$ref": "#/$defs/name" },
    "shipping_address": { "$ref": "https://example.com/schemas/address" }
  },
  "$defs": {
    "name": { "type": "string", "minLength": 1 }
  }
}
```

`$defs` reserves a reusable location. It has no direct validity effect.
Prefer `$defs` over obsolete `definitions`.

## Static references

`$ref` takes a URI-reference resolved against the current base URI.
Its result is the result of the referenced schema.
Other keywords alongside `$ref` in the same object also apply in 2020-12.

This is a breaking difference from draft-04 through draft-07, where siblings
of `$ref` were ignored.

## Base URI

Resolution follows RFC 3986:

- `$id` can establish a new base URI.
- Otherwise use the retrieval URI, encapsulating context, or an implementation
  default.
- `$id` must not contain a non-empty fragment. An empty fragment is discouraged
  retained compatibility syntax.
- Prefer absolute `$id` URIs. Relative `$id` values cannot resolve safely in
  anonymous schemas.
- `$id` values are identifiers. They do not guarantee network retrievability.
- Preload referenced schemas into a registry instead of assuming downloads.

## JSON Pointer fragments

A JSON Pointer fragment identifies a location by object keys and array indices:

```text
https://example.com/schemas/address#/properties/street_address
```

Escape `~` as `~0` and `/` as `~1`. Evaluate `~1` before `~0` when decoding.
Array index `-` means after the last element and normally fails normal instance
lookup.
An empty fragment means the whole document or resource.

Do not rely on a parent resource URI plus a pointer that crosses an embedded
`$id` boundary. Use the embedded resource canonical URI plus its local pointer.

## Anchors

```json
{
  "$id": "https://example.com/schemas/address",
  "properties": {
    "street_address": { "$anchor": "street", "type": "string" }
  }
}
```

`$anchor` creates a plain-name fragment independent of document structure.
A value such as `street` becomes `#street` against the containing resource URI.

Anchor names must start with a letter or underscore, followed by letters,
digits,
hyphens, underscores, or periods. Duplicate anchor names in one resource have
undefined behavior. Prefer `$anchor` for stable reuse and `$dynamicAnchor` only
for runtime extension.

## Retrieval versus canonical identity

A schema may be known by retrieval URI, `$id`, anchor URI, and pointer URI.
These can identify the same schema without being interchangeable for bundling,
debugging, or output purposes.

For output and error handling, preserve both:

- Keyword location along the validation path, including `$ref` and
  `$dynamicRef`.
- Absolute keyword location against the canonical resource URI where available.
- Instance location as a JSON Pointer.

## Compound documents and bundling

A document containing embedded `$id` resources is a compound schema document.
Each embedded resource is evaluated independently and may declare its own
dialect.

Safe bundling rules:

- Give every bundled resource an absolute `$id`.
- Copy resources under `$defs` or another schema-valued location.
- Do not replace the referencing object with the bundled resource.
- Do not wrap a bundled resource in unrelated applicators.
- Do not rewrite existing `$ref` values.
- Validate each resource against its own `$schema`, not the whole bundle against
  one meta-schema when dialects differ.
- Removing every `$ref` is not always safe because siblings, recursion,
  dynamics, and output locations can change meaning.

## Reference safety

- Reference targets under unknown keywords or non-schema values have undefined
  behavior.
- Direct self-reference cycles such as A referencing B referencing A can loop.
  Implementations must not hang.
- Do not treat every URI as downloadable. Some are pure identifiers such as
  `urn:` values.
- Report unresolved references as limitations. Do not claim validation succeeded
  normally when references were missing.
