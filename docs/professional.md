# Professional

Per-language block at `data.<locale>.professional`.

| Key | Type | Required | Notes |
| --- | --- | --- | --- |
| `role` | string | yes | The role best describing the candidate's current professional identity. |
| `role_start` | `{ year, month }` | yes | Used to compute the **career experience** duration shown next to the role. Represents how long the person has been working in the role they identify with — not the time at any specific company. |
| `summary` | string | yes | Short paragraph rendered in the **Profile** section of the resume. |
| `top_skills` | list[string] | yes (≥1) | Highlighted skills in the sidebar. |
| `skills` | list[string] | no | Additional skills shown as tags. |

## Duration formatting

Computed as full months from `role_start` to today.

- `< 12` months → `1 month`, `9 months`.
- `≥ 12` months → `2 years and 4 months`, with the months suffix omitted when zero (`3 years`).
- Brazilian Portuguese uses `1 ano e 1 mês`, `9 meses`, etc.
