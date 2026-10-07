# Objects and Arrays

Use this reference when constraining objects, properties, tuples, lists, or
containment.

## Objects

### Presence is not nullability

```json
{
  "type": "object",
  "properties": {
    "email": { "type": "string" }
  },
  "required": ["email"]
}
```

`{}` fails because `email` is missing. `{ "email": null }` fails because `null`
is not a string. To allow both missing and explicit null handling, use an
explicit
union such as `{ "type": ["string", "null"] }` where appropriate.

### Properties

`properties` validates values for listed names and ignores all other names.
It never requires presence. An empty object can therefore be valid.
Use `required` for presence and `additionalProperties` or
`unevaluatedProperties` for closure.

### Pattern properties

`patternProperties` keys are ECMA-262 expressions and are unanchored.
Use `^S_` rather than bare `S_` when prefix behavior is intended.
A property matching several patterns must satisfy every matching schema.

### Additional properties

`additionalProperties` sees only `properties` and `patternProperties` in the
same schema object. It cannot see declarations inside `allOf`, `anyOf`, `oneOf`,
`$ref`, conditionals, or other branches.

Consequence: placing `additionalProperties: false` in one branch and extending
elsewhere usually rejects the extension. Move closure outward, repeat
declarations,
or use `unevaluatedProperties` when cross-branch visibility is intended.

### Unevaluated properties

`unevaluatedProperties` can see successfully evaluated properties from adjacent
in-place applicators and references. This makes it suitable for extension and
conditional properties, but also sensitive to branch success.

Only successful evaluation marks a property evaluated. A property rejected by a
failed `anyOf` branch remains unevaluated.

### Property names and size

`propertyNames` validates every object key as a string instance.
`minProperties` and `maxProperties` take non-negative integers.
Omitted `minProperties` behaves as `0`.

## Arrays

### Lists

```json
{
  "type": "array",
  "items": { "type": "string" },
  "minItems": 1,
  "uniqueItems": true
}
```

Without `prefixItems`, `items` applies to every element. The empty array remains
valid unless `minItems` forbids it.

### Tuples

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "number" },
    { "type": "string" }
  ],
  "items": false,
  "minItems": 2,
  "maxItems": 2
}
```

`prefixItems` validates by position but does not require or limit length by
itself.
Short arrays may be valid and extra items may be valid. Add `items`, `minItems`,
`maxItems`, `unevaluatedItems`, or a combination thereof when exact shape
matters.

In 2020-12, `items` after `prefixItems` controls extra items. Do not use
obsolete
`additionalItems` in new 2020-12 schemas.

### Unevaluated items

`unevaluatedItems` can see successful evaluation from `prefixItems`, `items`,
`contains`, and adjacent in-place applicators. This allows half-open tuples and
extension patterns that `items` alone cannot express.

### Containment

```json
{
  "type": "array",
  "contains": { "type": "number" },
  "minContains": 2,
  "maxContains": 3
}
```

`contains` passes when at least one element matches, unless `minContains: 0`
makes the empty match explicitly valid. `minContains` and `maxContains` have no
effect without adjacent `contains`. Omitted `minContains` behaves as `1`.

Matching elements may also count as evaluated for `unevaluatedItems`.
Check the containing schema before combining `contains` with closed arrays.

### Length and uniqueness

`minItems` and `maxItems` take non-negative integers.
`uniqueItems: true` requires pairwise deep inequality.
`uniqueItems: false` and omission both impose no uniqueness requirement.
