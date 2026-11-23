# Languages

Per-language list at `data.<locale>.languages`. Each item:

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | Translated language name (e.g. `English`, `Inglês`). |
| `level` | enum | yes | `basic` \| `intermediate` \| `upper_intermediate` \| `advanced` \| `fluent` \| `native`. |

Levels are localized through the `language_level.*` translation keys.
