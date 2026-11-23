# Licenses & Certifications

Per-language list at `data.<locale>.certifications`. Each entry:

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `institution` | string | yes | Issuing organization. |
| `title` | string | yes | Certification name. |
| `start` | `{ year, month }` | yes | Issue date. |
| `end` | `{ year, month }` or `null` | no | Expiration date. `null` means it does not expire / still valid. |
| `credential_url` | URL | no | Link to the credential. |
| `bullets` | list[string] | no | Optional bullet points (skills covered, renewal notes). Rendered after the institution line when present. |
