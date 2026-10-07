# Keyword Index

Use this reference for keyword lookup, vocabulary membership,
value shape, and interactions.

The machine-readable registry is `assets/keyword-registry.json`.
It contains 57 distinct standard keywords. `format` appears
in both format vocabularies.

## Core vocabulary

| Keyword | Value | Behavior |
| --- | --- | --- |
| `$id` | URI-reference, no fragment | Identifier and base URI |
| `$schema` | Absolute URI | Dialect declaration, root only |
| `$ref` | URI-reference | Static applicator |
| `$anchor` | Plain-name fragment | Stable local identifier |
| `$dynamicRef` | URI-reference | Runtime-resolved applicator |
| `$dynamicAnchor` | Plain-name fragment | Dynamic extension point |
| `$vocabulary` | URI to boolean | Meta-schema only |
| `$defs` | Object of schemas | Reusable location |
| `$comment` | String | Maintainer note only |

## Applicator vocabulary

| Keyword | Value | Interaction |
| --- | --- | --- |
| `prefixItems` | Array of schemas | Tuple positions |
| `items` | Schema | Extra items after prefix |
| `contains` | Schema | At least one match |
| `additionalProperties` | Schema | Same object only |
| `properties` | Object of schemas | Matched values only |
| `patternProperties` | Regex to schema | Unanchored matches |
| `dependentSchemas` | Object of schemas | Whole instance on trigger |
| `propertyNames` | Schema | Validates key names |
| `allOf` | Array of schemas | Intersection |
| `anyOf` | Array of schemas | One or more |
| `oneOf` | Array of schemas | Exactly one |
| `not` | One schema | Negation |
| `if`, `then`, `else` | Schema each | `then`/`else` need `if` |

See `composition-and-evaluation.md` for `contains` and
closure interactions.

## Unevaluated vocabulary

| Keyword | Value | Interaction |
| --- | --- | --- |
| `unevaluatedItems` | Schema | Sees evaluated array items |
| `unevaluatedProperties` | Schema | Sees evaluated properties |

Only successful evaluation counts. Failed branches do not
mark locations evaluated.

## Validation vocabulary

| Keyword | Value | Applicability |
| --- | --- | --- |
| `type` | String or string array | Always checked |
| `const` | Any value | Equality |
| `enum` | Array | Equality, one member |
| `multipleOf` | Number over zero | Numbers only |
| `maximum`, `minimum` | Number | Inclusive bounds |
| `exclusiveMaximum` | Number | Exclusive upper bound |
| `exclusiveMinimum` | Number | Exclusive lower bound |
| `maxLength`, `minLength` | Integer, min zero | Strings only |
| `pattern` | ECMA-262 string | Strings, unanchored |
| `maxItems`, `minItems` | Integer, min zero | Arrays only |
| `uniqueItems` | Boolean | Arrays, deep equality |
| `maxContains` | Integer, min zero | Needs `contains` |
| `minContains` | Integer, min zero | Needs `contains`, default 1 |
| `maxProperties` | Integer, min zero | Objects only |
| `minProperties` | Integer, min zero | Objects only, default 0 |
| `required` | Unique string array | Missing, not `null` |
| `dependentRequired` | String arrays | One direction only |

Allowed `type` values are `array`, `boolean`, `integer`,
`null`, `number`, `object`, and `string`. `integer` means
zero fractional part. Non-applicable instances pass
type-specific assertions.

## Metadata vocabulary

`title`, `description`, `default`, `deprecated`,
`readOnly`, `writeOnly`, and `examples` are annotations.
They never change validity. `default` does not supply
missing values. `readOnly` and `writeOnly` do not
enforce access control.

## Format vocabularies

`format` is a string-valued annotation by default.
A separate assertion vocabulary exists, but default
2020-12 processing must not reject solely for an
invalid format. See `formats-and-content.md`.

## Content vocabulary

`contentEncoding`, `contentMediaType`, and
`contentSchema` are annotations for strings.
They do not automatically decode, parse, or
validate encoded content.
