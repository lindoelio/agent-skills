# Dynamic References

Use this reference for `$dynamicRef`, `$dynamicAnchor`, and extensible recursive
schemas.

## When dynamic references are needed

Use dynamic references when a recursive schema must remain extensible.
A static `$ref` always returns to the schema where it was written.
A dynamic reference can resolve to an overriding definition supplied by an outer
schema.

The canonical example is a generic tree extended by a strict tree.

## Minimal pattern

```json
{
  "$id": "https://example.com/tree",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$dynamicAnchor": "node",
  "type": "object",
  "properties": {
    "data": true,
    "children": {
      "type": "array",
      "items": { "$dynamicRef": "#node" }
    }
  }
}
```

```json
{
  "$id": "https://example.com/strict-tree",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$dynamicAnchor": "node",
  "$ref": "https://example.com/tree",
  "unevaluatedProperties": false
}
```

Validating with `strict-tree` makes nested `children` resolve dynamically to
`strict-tree#node`, not permanently to `tree#node`. Misspelled nested properties
therefore fail throughout the tree.

## Resolution rules

- Resolve `$dynamicRef` initially like `$ref`.
- If the starting fragment was created by `$dynamicAnchor`, replace it with the
  same-named dynamic anchor from the outermost schema resource in the dynamic
  scope.
- Otherwise behave as `$ref` with no runtime replacement.
- Dynamic scope follows evaluation, including traversed references. It is not
  the same as lexical nesting.
- Plain-name fragment matching ignores JSON Pointer structure. Moving an
  anchored schema under `$defs` does not break dynamic matching by itself.
- Do not use `$dynamicRef` for ordinary reuse. Prefer `$ref` and `$anchor`
  unless override behavior is required.

## Migration

Replace 2019-09 recursive keywords as follows:

- `$recursiveAnchor: true` becomes a named `$dynamicAnchor`, for example
  `"node"`.
- `$recursiveRef: "#"` becomes a named `$dynamicRef`, for example `"#node"`.
- Non-fragment URI-references are allowed as dynamic starting points in 2020-12.

Test both the base and extended schemas. A common regression is that the root is
strict
while children silently use the lenient base.

## Limits

Dynamic scope is advanced and easy to misuse. Avoid it in ordinary business
schemas.
Document the anchor name, base schema, override schema, and expected resolution
path
whenever dynamic references are introduced.
