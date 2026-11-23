# Experience

Per-language list at `data.<locale>.experience`. Each entry:

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `company` | string | yes | Company name. |
| `location` | string | no | City / region / country. |
| `company_size` | enum | no | `small` \| `mid` \| `big`. |
| `role` | string | yes | Role title at the company. |
| `start` | `{ year, month }` | yes | Start month. |
| `end` | `{ year, month }` or `null` | no | `null` (or omitted) means the candidate is still working there ("Present"). |
| `description` | string | no | Free-form summary paragraph. |
| `bullets` | list[string] | no | Optional achievement bullets. Rendered after `description` when present. |

Dates are rendered using the locale-aware month/year format (Babel). The same bullet list pattern exists on **education**, **certifications**, **side project** and **open source project** entries — see [education.md](education.md), [certifications.md](certifications.md), [side-projects.md](side-projects.md) and [open-source-projects.md](open-source-projects.md).
