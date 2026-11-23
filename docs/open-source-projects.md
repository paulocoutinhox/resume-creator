# Open Source Projects

Per-language list at `data.<locale>.open_source_projects`. Each entry:

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `title` | string | yes | Project name. |
| `description` | string | yes | Short description. |
| `url` | URL | no | Project link. |
| `start` | `{ year, month }` | yes | Project start. |
| `end` | `{ year, month }` or `null` | no | `null` means it is ongoing. |
| `bullets` | list[string] | no | Optional bullet points (stack, outcomes). Rendered after `description` when present. |
