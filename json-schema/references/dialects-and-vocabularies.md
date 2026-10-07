# Dialects and Vocabularies

Use this reference when declaring `$schema`, validating schemas, combining
vocabularies, or adding custom keywords.

## Declare the dialect

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "type": "object"
}
```

Rules:

- Put `$schema` at the document root. It must not appear in ordinary
  non-resource subschemas.
- Embedded resources may declare their own `$schema`.
- Referenced schemas need their own `$schema`. A parent `$schema` does not
  travel across `$ref`.
- If `$schema` is absent, behavior is implementation-defined. Do not assume
  2020-12 silently.
- Always include `$schema` and an absolute `$id` in durable schemas.

The default 2020-12 dialect requires core, applicator, unevaluated, validation,
metadata, format-annotation, and content vocabularies.

## Meta-schemas

A meta-schema is a schema for schemas. The root 2020-12 meta-schema composes the
single-vocabulary meta-schemas vendored under `assets/official-metaschemas/`.

Meta-schema checks establish syntax, not complete correctness. A schema can pass
meta-schema validation while still having:

- Unresolved `$ref` or `$dynamicRef` targets.
- Unsupported vocabularies or custom keywords.
- Unsatisfiable combinations.
- Missing application-required constraints.

Validate schemas and instances separately. Report reference resolution
separately.

## Vocabularies

`$vocabulary` appears in meta-schemas, not ordinary schemas. Each entry maps a
vocabulary URI to whether implementation understanding is required:

```json
{
  "$vocabulary": {
    "https://json-schema.org/draft/2020-12/vocab/core": true,
    "https://json-schema.org/draft/2020-12/vocab/validation": true
  }
}
```

Rules:

- Core is mandatory and cannot meaningfully be optional.
- Required unknown vocabulary means refuse processing.
- Optional unknown vocabulary means implementations SHOULD proceed, treating
  unknown keywords as annotations.
- Vocabulary declarations are not inherited through `$ref`. Repeat them in every
  meta-schema that needs them.
- Do not declare conflicting vocabularies that define the same keyword
  differently.

## Custom keywords and dialects

Custom keywords are possible, but interoperability depends on category:

- Safest: metadata-like annotations that do not affect validity.
- Moderate: assertions that do not apply subschemas or alter existing keywords.
- Least portable: applicators or keywords that change existing keyword behavior.

Every environment using the schema must understand the custom semantics.
Provide a meta-schema for syntax and separate documentation or code for
semantics.
Use a URI under a domain you control. Never reuse an official draft URI for a
custom dialect.

Unknown keywords without implementation support SHOULD be treated as annotations
by default.
They do not fail validation and their application behavior is undefined if they
appear to contain subschemas.
