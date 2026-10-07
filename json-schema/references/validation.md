# Validation

Use this reference for type, numeric, string, enum, and const behavior.

## Schema forms

A schema is an object or boolean. `{}` and `true` accept any valid JSON.
`false` and `{ "not": {} }` reject everything. Empty or unknown-only objects
accept everything and produce annotation-only behavior.

## Instance model

Instance types are `null`, `boolean`, `object`, `array`, `number`, and `string`.
`integer` is a validation word for a number with zero fractional part, not a
separate
data-model type. `1` and `1.0` are therefore both integers.

Equality is type-sensitive and mathematical for numbers. Object member order is
insignificant. Formatting differences, including trailing zeros, do not matter.

## Type

Valid values:

```json
{ "type": "string" }
```

```json
{ "type": ["string", "null"] }
```

Rules:

- `type` accepts one allowed string or a unique array of allowed strings.
- There is no `regular expressions` type despite one guide saying otherwise.
- `number` includes integers. `integer` accepts `1.0` but rejects `1.5` and
  `"1"`.
- Most other validation keywords ignore instances outside their target type.
- Therefore `{ "type": ["string", "null"], "maxLength": 255 }` permits `null`.

## Enum and const

```json
{ "enum": ["red", "amber", "green"] }
```

```json
{ "const": "United States of America" }
```

Rules:

- `enum` takes an array and passes when the instance equals one member.
- `const` passes when the instance equals its value.
- Members may use any JSON type, including `null`, objects, and arrays.
- Deep equality applies. Object key order does not matter.

## Numbers

```json
{
  "type": "number",
  "minimum": 0,
  "exclusiveMaximum": 100,
  "multipleOf": 0.01
}
```

Rules:

- `multipleOf` must be strictly greater than zero.
- `minimum` and `maximum` are inclusive. `exclusiveMinimum` and
  `exclusiveMaximum` are exclusive.
- Combining inclusive and exclusive bounds for the same direction is redundant.
- Do not use draft-04 boolean `exclusiveMinimum: true` in 2020-12.
- JSON imposes no precision bound, but implementations may have numeric limits.
  State the runtime when precision matters.

## Strings

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 3,
  "pattern": "^[A-Z]{3}-\\d{3}$"
}
```

Rules:

- Length counts Unicode characters, not bytes or grapheme clusters in every
  runtime.
- Omitted `minLength` behaves as `0`.
- `pattern` uses ECMA-262 and is unanchored. `"p"` matches `"apple"`.
- Anchor intentionally with `^` and `$` when a full-string match is wanted.
- Prefer the portable regex subset: literals, classes, quantifiers, anchors,
  grouping, and alternation.
- Unicode support is expected but not strictly guaranteed. Avoid
  implementation-only constructs in portable schemas.
