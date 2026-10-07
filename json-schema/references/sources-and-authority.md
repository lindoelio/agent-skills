# Sources and Authority

Use this reference before citing behavior, changing dialects, or resolving
conflicting documentation.

## Source hierarchy

- Normative semantics: released Draft 2020-12 Core and Validation
  specifications.
- Syntax shape: official 2020-12 meta-schemas in `assets/official-metaschemas/`.
- Explanation: official Understanding JSON Schema guides and reference chapters.
- Behavior of one tool: that tool's documentation and version notes.
- Community examples, blogs, model knowledge, and unreleased drafts: lowest
  authority.

When sources conflict, the released specification wins. Record the conflict
explicitly.

## Pinned sources

Source URIs, versions, retrieval dates, and content digests are pinned in
`assets/source-manifest.json`.
The current published dialect is 2020-12, published 16 June 2022.
Do not mix unreleased GitHub specification sources into 2020-12 work.

Core specification sections:

- Data model, equality, schema forms: Core Sec. 4
- Keyword categories and evaluation: Core Sec. 7
- `$schema`, `$vocabulary`, `$id`, anchors, references, `$defs`, `$comment`:
  Core Sec. 8
- Loading, dereferencing, compound documents: Core Sec. 9
- Applicators: Core Sec. 10
- Unevaluated locations: Core Sec. 11
- Output: Core Sec. 12
- Security: Core Sec. 13

Validation specification sections:

- Type, enum, const: Validation Sec. 6.1
- Numeric constraints: Validation Sec. 6.2
- String constraints: Validation Sec. 6.3
- Array constraints: Validation Sec. 6.4
- Object constraints: Validation Sec. 6.5
- Format vocabularies and defined formats: Validation Sec. 7
- Encoded content: Validation Sec. 8
- Metadata: Validation Sec. 9

Supporting standards:

- JSON Pointer escaping and evaluation: RFC 6901
- Relative JSON Pointer: draft-bhutton-relative-json-pointer-00
- URI resolution: RFC 3986 Sec. 5

## Known documentation discrepancies

Do not copy these without correction:

- One guide lists `regular expressions` as a `type` value. Valid `type` values
  are `array`, `boolean`, `integer`, `null`, `number`, `object`, and `string`.
- One composition overview implies `not` takes an array. `not` takes exactly one
  schema.
- Some guide examples use obsolete `additionalItems`, `definitions`,
  `dependencies`, `id`, boolean `exclusiveMinimum`/`exclusiveMaximum`, or
  placeholders such as `"... etc ..."`.
- `format` guidance varies by implementation. Default 2020-12 behavior is
  annotation-first.
- Meta-schema validity does not prove references resolve, vocabularies are
  supported, or application requirements are complete.

## Citation rules

- Cite consequential semantic claims, for example `Core Sec. 10.2.1.1 allOf`.
- Preserve `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` exactly.
- State whether a dialect was declared in `$schema` or assumed by the agent.
- Separate standard 2020-12 behavior from Hyper-Schema, OpenAPI, vendor
  extensions, and validator options.
- If a source cannot be checked, say so instead of guessing.
