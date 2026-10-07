# Formats and Content

Use this reference for `format`, `contentEncoding`, `contentMediaType`, and
`contentSchema`.

## Format default

Under the default 2020-12 dialect, `format` is annotation-first:

```json
{
  "type": "string",
  "format": "email"
}
```

An invalid email string still validates successfully unless format assertion has
been explicitly enabled through the format-assertion vocabulary or an
implementation option. Always state which behavior was used.

Rules:

- `format` values are strings.
- Formats generally apply to strings. Non-string instances are ignored for
  string formats.
- Unknown formats are annotations. Do not fail default validation for them.
- Custom formats are allowed only by agreement. Prefer a custom keyword if
  interoperability matters.
- Format-assertion processing requires full syntactic support and refusal when
  an asserted format is unknown or unsupported.
- Implementation coverage varies, especially for `email`, `hostname`, and
  `regex`.

## Defined 2020-12 formats

Dates and times: `date-time`, `date`, `time`, `duration`.
Email: `email`, `idn-email`.
Hostnames: `hostname`, `idn-hostname`.
IP addresses: `ipv4`, `ipv6`.
Resource identifiers: `uri`, `uri-reference`, `iri`, `iri-reference`, `uuid`.
URI template: `uri-template`.
JSON pointers: `json-pointer`, `relative-json-pointer`.
Regular expression: `regex`.

Do not use these names for incompatible custom formats.

## Content annotations

```json
{
  "type": "string",
  "contentMediaType": "image/png",
  "contentEncoding": "base64"
}
```

```json
{
  "type": "string",
  "contentMediaType": "application/json",
  "contentSchema": {
    "type": "object",
    "required": ["name"],
    "properties": {
      "name": { "type": "string" }
    }
  }
}
```

Rules:

- All content keywords apply only to strings. Other instance types ignore them.
- Malformed encoded content does not make the containing string invalid by
  itself.
- Implementations must not automatically decode, parse, or validate by default.
- Separate automatic processing, when offered, must report encoded-document
  results separately from container validation.
- `contentSchema` is ignored without `contentMediaType`.
- An absent `contentEncoding` with present `contentMediaType` means identity
  encoding.
- `base64`, `base32`, `base16`, and MIME transfer encodings may appear. They are
  distinct from HTTP content encoding.
- Decoding untrusted embedded media can expose parser, resource, and script
  vulnerabilities. Process it only with an established schema-instance trust
  relationship.
