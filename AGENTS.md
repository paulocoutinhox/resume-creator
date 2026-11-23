# AGENTS.md

Guide for coding agents working on Resume Creator. Read it before changing code or resume content.

## What the project does

Resume Creator turns one YAML configuration into a print-ready PDF and a responsive website for each configured language.

1. `main.py` starts the Click CLI in `modules/cli.py`.
2. `modules/config/loader.py` reads `data/config.yml`, loads every locale file listed under `data:` and validates everything with the Pydantic models in `modules/models/resume.py`. It also checks that `site.theme.pdf` and `site.theme.web` exist in the theme registry and target the right output.
3. `modules/commands/build.py` builds a `ThemeContext` per locale and asks the registry (`modules/themes/registry.py`) for the configured theme.
4. The theme renders Jinja templates to HTML. Every visible label comes from `t()` (`modules/i18n/translator.py`), and dates and durations come from `modules/utils/`.
5. PDF: `modules/generators/pdf.py` sends the HTML to WeasyPrint and writes `build/pdf/<basename>-<locale>.pdf`. Fonts and the photo are embedded as data URIs, so the PDF is self-contained.
6. Web: the HTML is written to `frontend/generated/`, Vite and Tailwind CSS 4 build `build/web/assets/`, and the pages are copied to `build/web/<locale>/index.html`, plus a root redirect to the default language.

## Project structure

```
main.py                     CLI entry point
requirements.txt            Python dependencies (pip)
data/
  config.yml                languages, default language, output name, themes, photo, locale files
  locales/<locale>.yml      the resume content for one language
  img/                      profile photo
modules/
  cli.py                    commands: build [pdf|web], validate, serve
  commands/                 one file per command
  config/loader.py          YAML loading and validation
  models/
    enums.py                every closed set of values (locales, levels, sizes, networks, icons)
    resume.py               strict Pydantic schema of the whole configuration
  i18n/
    translator.py           t(key) lookup, fails on missing keys
    locales/<locale>.yml    fixed UI strings (section titles, labels)
  themes/
    base.py                 Theme base class, ThemeContext, Jinja environment and globals
    registry.py             theme name -> class, output type checks
    icons.py, fonts.py      shared icon and font helpers
    modern_pdf/             PDF theme: theme.py, templates/, styles/pdf.css, fonts/
    modern_web/             web theme: theme.py, templates/ (one file per section)
  generators/               pdf.py (WeasyPrint) and web.py (HTML writer)
  utils/                    dates.py (Babel month/year formats), duration.py (career duration)
frontend/                   Vite + Tailwind CSS 4 project for the web assets
docs/                       field-by-field reference, one file per resume section
.github/workflows/build.yml CI: builds PDFs and site, uploads them as artifacts
Dockerfile                  full toolchain image (Python, WeasyPrint libraries, Node.js)
```

`build/`, `frontend/generated/` and `frontend/node_modules/` are generated and ignored by Git.

## Commands

```bash
pip install -r requirements.txt
python main.py validate        # validate data/config.yml and print a section summary
python main.py build           # PDFs and website for every language
python main.py build pdf       # PDFs only
python main.py build web       # website only (installs frontend packages on first run)
python main.py serve           # preview build/web on http://127.0.0.1:4173
```

Requirements: Python 3.13, Node.js 22 for the web build, and the WeasyPrint native libraries (Pango, Cairo, GDK-Pixbuf). On macOS with Homebrew, if WeasyPrint cannot find `libgobject`, run with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`.

Dependencies are managed with `pip` and `requirements.txt` with exact versions. Keep it that way unless the maintainer asks for something else.

There is no test suite. Verify every change with `python main.py validate` and `python main.py build`, then open the generated PDFs and pages and check the layout.

## Code standards

- Python 3.13 with type hints on every function signature and return value. Use `X | None`, `list[str]` and `pathlib.Path`.
- Schema models extend `StrictModel` (`extra="forbid"`, `str_strip_whitespace=True`, `frozen=True`). Unknown or misspelled YAML keys must fail validation, never be ignored.
- Every closed set of values is an `Enum` in `modules/models/enums.py`. Do not compare against loose strings.
- Private helpers and module constants start with `_` (`_build_pdfs`, `_PROJECT_ROOT`). Public functions keep short, direct names (`load_config`, `run_build`).
- Errors use dedicated exception classes (`ConfigLoadError`, `TranslationError`, `UnknownThemeError`) with messages that say what was wrong and what was expected. Fail early and loudly; never fall back silently.
- Read and write files with explicit `encoding="utf-8"`.
- Comments are lowercase and explain why, not what.
- Jinja runs with `StrictUndefined`. Templates never hardcode visible text: add a key to every file in `modules/i18n/locales/` and call `t()`.
- Templates render only what the YAML provides. Optional fields are wrapped in `{% if %}` so nothing empty or invented appears.
- Formatting follows `.editorconfig`: 4 spaces for Python and HTML, 2 for YAML, LF line endings, final newline.
- Terminal output goes through `rich.console.Console`.

## Adding or changing a resume section

A section touches every layer. For a new list section (for example `open_source_projects`):

1. Model: add the entry class and the field on `LocalizedResume` in `modules/models/resume.py`.
2. Validation summary: add the count in `modules/commands/validate.py`.
3. UI strings: add `section.<key>` to every file in `modules/i18n/locales/`.
4. PDF: add the block to `modules/themes/modern_pdf/templates/main.html` (or `sidebar.html`).
5. Web: add `modules/themes/modern_web/templates/<key>.html` and include it in `layout.html`.
6. Docs: add `docs/<key>.md`, link it in `README.md`, and update `docs/i18n.md`, `docs/experience.md` and `docs/themes.md` where sections are listed.
7. Keep existing sections working. Removing or renaming a key breaks other people's resumes, so only do it when explicitly asked.

## Writing resume content

The content in `data/locales/` is read by recruiters and hiring managers. Every text must help them understand, in a few seconds, what the person is good at and what problems they solve.

### What companies look for

- **Core first.** The profile summary says who the person is professionally and what their core is, in three to five short sentences, one idea each. It does not list every technology they ever touched; secondary skills go in the skills list, experience or projects.
- **Solutions, not duties.** Each experience shows what the person built or solved: the problem, what they did and the result. Prefer "Built the shared C++ SDK used by the iOS and Android apps" over "Responsible for mobile development".
- **Context in one line.** The experience `description` gives the company and product context (what it is, its scale) in one sentence. The `bullets` hold the solutions, one per bullet, short.
- **Projects explain their value.** An open source or side project says what it does, which problem it removes for its users and any real result (adoption, stars, performance, who uses it).
- **Skills are scannable.** `top_skills` holds the professional roles or strengths that define the person. `skills` holds concrete languages, platforms and tools, one per tag.
- **Real facts only.** Use numbers, results and claims only when they can be verified in the existing resume, the person's repositories or what the person said. Never invent metrics, clients or results. When a fact is missing, ask.

### Sound like a person, not like AI

- Write plainly, with short sentences and common words.
- Avoid buzzwords and filler: "passionate", "cutting-edge", "robust", "seamless", "leverage", "spearheaded", "innovative", "results-driven", "dynamic", "synergy" and their Portuguese equivalents ("apaixonado", "inovador", "robusto", "alavancar", "sinergia").
- Do not stack lists of three adjectives or three nouns in every sentence, and do not decorate titles with dashes or slogans.
- Do not repeat the same idea in the summary, the experience and the projects.

### Per language

Each locale file is written for the job market of its language, not translated word for word. Translate the meaning and keep both files in sync: same entries, same facts, same order.

- **English (`en`)**, international and US market: short, results-focused, no personal opinions, implied first person. Bullets either name the solution ("Ubook Mobile SDK: shared C++ core for audio, sync and DRM") or start with a past-tense action verb ("Built", "Led", "Shipped"); keep one style within an entry. US and UK recruiters usually do not expect a photo, birth date or citizenship.
- **Brazilian Portuguese (`pt`)**: natural Brazilian Portuguese as used by tech recruiters, with technical terms that the market keeps in English (iOS, back-end, deploy, SDK, streaming). Bullets either name the solution or start with a first-person verb ("Desenvolvi", "Liderei"); keep one style within an entry. Photo and personal details are common in Brazilian resumes.
- Personal data (photo, birth date, citizenship, pronouns) is the person's choice. Never add or remove it on your own; mention market differences when relevant.
- Dates, durations and section titles are formatted by the generator for each locale. Do not write them inside the text.
