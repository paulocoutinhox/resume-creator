# CLI

All commands run through `python main.py`.

| Command | Description |
| --- | --- |
| `python main.py build` | Build PDFs and the web bundle for every configured language. |
| `python main.py build pdf` | Build only the PDF outputs. |
| `python main.py build web` | Build only the web bundle (Vite + Tailwind). |
| `python main.py validate` | Validate `data/config.yml` against the strict schema, ensure `site.theme.pdf` and `site.theme.web` reference registered themes, and print a section summary. |
| `python main.py serve` | Serve `build/web` locally for preview. Defaults: `--host 127.0.0.1 --port 4173`. |

All commands except `serve` accept `--config PATH` to point at a different YAML file. `serve` accepts `--host` and `--port` (defaults: `127.0.0.1` and `4173`).

## Outputs

- `build/pdf/<output_basename>-<locale>.pdf` — one PDF per language declared in `site.languages`.
- `build/web/<locale>/index.html` — one HTML per language.
- `build/web/index.html` — meta-refresh redirect to `site.default_language`.
- `build/web/assets/main.css`, `build/web/assets/main.js` — produced by Vite.
- `build/web/assets/photo.<ext>` — copy of `assets.photo` used by the web build.
- `build/web/assets/favicon/` and other files under `frontend/public/` — copied as static assets by Vite into `build/web/assets/`.
