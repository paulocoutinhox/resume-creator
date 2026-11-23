# Themes

Each output type has its own dedicated theme. Themes live under `modules/themes/<theme_name>/` and subclass `modules.themes.base.Theme`. Every theme declares the single `ThemeOutputType` it targets (`PDF` or `WEB`), and the registry refuses to use a theme for the wrong output.

The repository ships with two themes:

- **Modern PDF** (`modern-pdf`) — A4, two-column layout (dark navy sidebar with photo, contact, social, languages and skills; white main column with name, role, profile summary, work experience, education, certifications, side projects and open source projects). Optimised for WeasyPrint, with its typography bundled as WOFF2 and embedded into every PDF as data URIs.
- **Modern Web** (`modern-web`) — A long-form, card-based reading experience built with Tailwind CSS 4. Sticky header with photo, name and language switcher; large hero with name, role and summary; section cards for experience, education, certifications, side projects, open source projects, skills, languages, contact and footer. Uses a system font stack (no remote fonts).

## Selecting themes

```yaml
site:
  theme:
    pdf: modern-pdf
    web: modern-web
```

`site.theme.pdf` is used by `python main.py build pdf` and `site.theme.web` by `python main.py build web`.

## Building a custom theme

1. Create `modules/themes/<name>/theme.py` with a `Theme` subclass:
   - `name`: unique identifier referenced from `site.theme.pdf` or `site.theme.web`.
   - `output_type`: either `ThemeOutputType.PDF` or `ThemeOutputType.WEB`.
   - `template_root`: folder containing the Jinja templates.
   - `render()`: returns the final HTML string.
2. Register the class in `modules/themes/registry.py`.
3. The theme receives a `ThemeContext` with the localized resume, the locale, the photo URI (data URI for PDF, relative path for Web) and the asset base URL.

## Assets

`assets.photo` is a path relative to the project root. For PDFs the file is embedded as a base64 `data:` URI. For the web build it is copied to `build/web/assets/photo.<ext>` and referenced relatively.

## Fonts

Fonts are part of the theme. The PDF theme bundles WOFF2 files under its own `fonts/` folder and embeds them in the rendered HTML as `@font-face` data URIs, so the resulting PDF is self-contained and renders identically regardless of the host system. The web theme relies on the system font stack (no remote font requests) for fast load and consistent rendering across operating systems.

### Swapping the PDF font

Any font that can be exported to WOFF2 works. To swap:

1. Drop the new `.woff2` files into `modules/themes/modern_pdf/fonts/`.
2. Edit `modules/themes/modern_pdf/theme.py` and update `FONT_FAMILY` and the `FONT_FACES` tuple (one `FontFace(family, weight, style, filename)` entry per file).
3. Update the `font-family` declaration in `modules/themes/modern_pdf/styles/pdf.css` to match the new family name.

The shared helper `modules.themes.fonts.embed_font_faces` handles the data URI embedding for any theme, so custom themes can declare their own `FONT_FACES` the same way.
