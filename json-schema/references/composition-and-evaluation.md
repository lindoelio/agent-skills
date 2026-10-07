# Composition and Evaluation

Use this reference for boolean combination, conditionals, dependencies, and
evaluation behavior.

## Boolean combination

```json
{ "allOf": [{ "type": "string" }, { "maxLength": 5 }] }
```

```json
{ "anyOf": [{ "type": "string" }, { "type": "number" }] }
```

```json
{ "oneOf": [{ "multipleOf": 5 }, { "multipleOf": 3 }] }
```

```json
{ "not": { "type": "string" } }
```

Rules:

- `allOf`, `anyOf`, and `oneOf` take non-empty arrays of schemas.
- `not` takes exactly one schema, not an array.
- `allOf` requires every branch to pass. It does not merge object schemas.
- `anyOf` requires one or more branches to pass.
- `oneOf` requires exactly one branch to pass. Overlapping branches such as
  multiples of both 3 and 5 fail.
- `not` passes when its subschema fails.
- Sibling subschemas are independent. One branch result must not alter another
  branch result.
- Impossible intersections such as string and number are valid schemas that
  reject everything.

## Conditionals

```json
{
  "type": "object",
  "if": {
    "properties": { "country": { "const": "Canada" } },
    "required": ["country"]
  },
  "then": {
    "properties": {
      "postal_code": {
        "pattern": "^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$"
      }
    }
  },
  "else": {
    "properties": { "postal_code": { "pattern": "^[0-9]{5}(-[0-9]{4})?$" } }
  }
}
```

Rules:

- `if` controls selection. It has no direct validity effect by itself.
- `then` applies only when `if` passes. `else` applies only when `if` fails.
- `then` and `else` without `if` are ignored entirely and must not be evaluated.
- `if`, `then`, and `else` do not pair across subschema boundaries.
- Include `required: ["country"]` in `if` when absence should select `else`.
- For more than two branches, use separate `allOf` entries containing
  independent `if`/`then` pairs.

## Dependencies

`dependentRequired` maps a present property to other required properties.
It is unidirectional unless both directions are declared.

`dependentSchemas` maps a present property to a schema applied to the whole
instance.
Like `allOf`, it applies independently and merges nothing.

Obsolete `dependencies` combined both behaviors. Use the split 2020-12 keywords
in new work.

## Evaluation model

- Assertions produce boolean results.
- Annotations attach information and are available only from successful schema
  locations.
- Applicators apply subschemas in place or to child locations and combine
  results.
- Keywords in one object are adjacent. Missing keywords produce no assertion,
  annotation, or subschema evaluation.
- Type-specific assertions pass for instances outside their target type.
- Annotation collection may require evaluating branches that cannot alter the
  final boolean result.
- Unknown keywords SHOULD be treated as annotations. Their values are retained
  as annotation values but have no standard validity effect.
- Boolean schemas never produce annotations.
- Guard against infinite recursion. Mutually recursive `allOf` references have
  undefined behavior.
