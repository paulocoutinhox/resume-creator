# Education

Per-language list at `data.<locale>.education`. Each entry:

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `level` | enum | yes | `high_school` \| `unfinished_bachelor` \| `two_year` \| `bachelor` \| `post_graduation` \| `mba` \| `master` \| `doctoral` \| `post_doctoral`. |
| `institution` | string | yes | School / university. |
| `title` | string | yes | Degree / program title. |
| `start` | `{ year, month }` | yes | Start month. |
| `end` | `{ year, month }` or `null` | no | `null` means ongoing. |
| `description` | string | no | Free-form description. |
| `bullets` | list[string] | no | Optional bullet points (highlights, coursework, honours). Rendered after `description` when present. |
