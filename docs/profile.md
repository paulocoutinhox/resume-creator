# Profile

Per-language block at `data.<locale>.profile`.

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | Full name. The web header shows `<first> <last>`. |
| `email` | string | yes | Rendered as `mailto:` link. |
| `phone` | string | no | Rendered as `tel:` link. |
| `whatsapp` | string | no | Rendered as `https://wa.me/<digits>` link. |
| `location` | string | no | Free-form, e.g. `City, State, Country`. |
| `citizenship` | string | no | Country of citizenship. |
| `gender` | enum | no | `male` \| `female` \| `other`. |
| `pronouns` | enum | no | `he/him` \| `she/her` \| `they/them` \| `custom`. |
| `pronouns_custom` | string | only with `custom` | Required when `pronouns: custom`, forbidden otherwise. |
| `birth` | `{ year, month, day? }` | no | Optional date of birth. `day` is optional, allowing month/year only when you don't want to expose the exact day. |

Any field left out simply does not render. Photo lives in `assets.photo` (see [themes.md](themes.md)).
