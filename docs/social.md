# Social

Per-language list at `data.<locale>.social`. Each item:

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `network` | enum | yes | `linkedin` \| `github` \| `site` \| `youtube` \| `instagram` \| `x`. |
| `url` | URL | yes | Full `https://` URL. |
| `handle` | string | no | Display label (e.g. `@paulocoutinhox`). Falls back to the URL when omitted. |

Each entry renders with the matching brand icon and is linked with `target="_blank"`.
