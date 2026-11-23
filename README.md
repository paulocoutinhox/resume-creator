<p align="center">
    <a href="https://github.com/paulocoutinhox/resume-creator" target="_blank" rel="noopener noreferrer">
        <img width="180" src="extras/images/logo.png" alt="Resume Creator Logo">
    </a>
</p>


# Resume Creator

[![Build](https://github.com/paulocoutinhox/resume-creator/actions/workflows/build.yml/badge.svg)](https://github.com/paulocoutinhox/resume-creator/actions/workflows/build.yml)

Generate a polished, print-ready **PDF** and a responsive **website** for your resume from a single configuration file. Write your information once and get matching outputs for every language you turn on.

## ✨ What it does

- Builds a print-ready PDF you can send as-is.
- Builds a responsive site for the same content, tuned for phones, tablets and desktops.
- Produces one PDF and one site per language you configure, from the same source data.
- Fills the layouts from your YAML only where you supplied values — nothing empty is invented or shown as filler.
- Derives career experience from your role start date and formats labels and durations in each locale.
- Uses deep links so taps and clicks work the same in the PDF and on the site.
- Ships with separate built-in looks for print and for the web; you can add or swap themes.
- Includes Docker and a GitHub Actions workflow so CI can build everything and publish artifacts.

## 🌐 Supported languages

Content and fixed UI strings are available for:

- **English** (`en`)
- **Brazilian Portuguese** (`pt`)

You choose which of these are built and which is the default in your configuration file.

## 🚀 Your resume in a few steps

Follow this order so nothing is missing when you generate your files.

1. **Fork the repository** on GitHub (or create your own copy) so you have a project you can change freely.
2. **Clone your fork** to your computer and open a terminal in that folder.
3. **Install dependencies** — Python 3.13, a virtual environment, `pip install -r requirements.txt`, and Node.js 22 for website builds. Use the **Quickstart** commands below; the first `build web` or full `build` installs frontend packages automatically.
4. **Edit `data/config.yml`** — set `site.languages`, `site.default_language`, `site.output_basename`, optional `assets.photo`, and the `data:` map that points each language code to a file under `data/locales/`.
5. **Edit your locale files** under `data/locales/` (for example `en.yml` and `pt.yml`) — replace the sample profile, summary, experience, education, and everything else with your own content. Paths in `data:` are relative to the folder where `config.yml` lives.
6. **Check and build** — run `python main.py validate`, then `python main.py build`. PDFs appear under `build/pdf/` and the site under `build/web/`. Use `python main.py serve` after a web build to preview locally. When you push your fork to GitHub, the workflow under **GitHub Actions** can produce the same artifacts for you.

Field-by-field reference for the YAML lives in [`docs/`](docs/) (profile, experience, themes, and so on).

### 🗣️ Using only one language

If you want a single language (for example English only):

- In `data/config.yml`, set `site.languages` to one entry, e.g. `[en]`, and set `site.default_language` to that same code (`en`).
- Under `data:`, keep **only** that locale, e.g. `en: locales/en.yml`, and point it to the file you maintain.
- You can remove the other locale file from `data/locales/` if you no longer need it, or leave it on disk unused — it must not appear under `data:` unless it is also listed in `site.languages`.

The generator always builds one PDF and one site folder per entry in `site.languages`.

## ⚙️ Requirements

- Python 3.13+
- Node.js 22 LTS (only used to build the web output)

WeasyPrint also needs a few native libraries on Linux. On Debian/Ubuntu:

```bash
sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2 \
    libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info fonts-dejavu fonts-liberation
```

## 💻 Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python main.py validate           # validates data/config.yml
python main.py build              # builds the PDFs and the website
python main.py build pdf          # PDFs only
python main.py build web          # website only
python main.py serve              # preview the website locally
```

Outputs land under `build/`:

- `build/pdf/<basename>-<locale>.pdf` — one PDF per language.
- `build/web/<locale>/index.html` — one website per language, plus a root redirect to your default language.

## 🐳 Docker

```bash
docker build -t resume-creator .
docker run --rm -v "$PWD/data:/app/data" -v "$PWD/build:/app/build" resume-creator
docker run --rm -v "$PWD/data:/app/data" -v "$PWD/build:/app/build" resume-creator build pdf
```

Any CLI subcommand works after the image name.

## 🔄 GitHub Actions

The included workflow builds the project on every push and uploads two artifacts:

- `resume-pdf` — every generated PDF.
- `resume-web` — the full website.

## 📚 Configuration

Your data lives in `data/config.yml` plus one file per language under `data/locales/`. The full schema is documented per section in [`docs/`](docs/):

- [docs/cli.md](docs/cli.md)
- [docs/profile.md](docs/profile.md)
- [docs/professional.md](docs/professional.md)
- [docs/social.md](docs/social.md)
- [docs/languages.md](docs/languages.md)
- [docs/experience.md](docs/experience.md)
- [docs/education.md](docs/education.md)
- [docs/certifications.md](docs/certifications.md)
- [docs/side-projects.md](docs/side-projects.md)
- [docs/open-source-projects.md](docs/open-source-projects.md)
- [docs/themes.md](docs/themes.md)
- [docs/i18n.md](docs/i18n.md)
- [docs/docker.md](docs/docker.md)

## ☕ Buy me a coffee

If this project saved you time, consider supporting its development:

<a href="https://ko-fi.com/A0A412XEV" target="_blank" rel="noopener noreferrer"><img height="36" style="border:0;height:36px;" src="https://storage.ko-fi.com/cdn/kofi2.png?v=6" alt="Buy Me a Coffee at ko-fi.com"></a>

*Made with ❤️ by Paulo Coutinho.*

## 📜 License

MIT
