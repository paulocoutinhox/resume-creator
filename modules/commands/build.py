import shutil
import subprocess
from pathlib import Path

from rich.console import Console

from modules.config.loader import load_config
from modules.generators.pdf import render_pdf
from modules.generators.web import render_web_html
from modules.models.enums import Locale, ThemeOutputType
from modules.models.resume import ResumeConfig
from modules.themes.base import ThemeContext, file_to_data_uri
from modules.themes.registry import build_theme


_console = Console()


class BuildPaths:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.build_dir = project_root / "build"
        self.pdf_dir = self.build_dir / "pdf"
        self.web_dir = self.build_dir / "web"
        self.web_assets_dir = self.web_dir / "assets"
        self.frontend_dir = project_root / "frontend"
        self.generated_dir = self.frontend_dir / "generated"


def run_build(project_root: Path, config_path: Path, targets: tuple[str, ...]) -> None:
    config = load_config(config_path)
    paths = BuildPaths(project_root)

    if "pdf" in targets:
        _build_pdfs(paths, config)

    if "web" in targets:
        _build_web(paths, config)


def _resolve_photo(project_root: Path, config: ResumeConfig) -> Path | None:
    photo = config.assets.photo
    if photo is None:
        return None
    candidate = photo if photo.is_absolute() else (project_root / photo)
    if not candidate.is_file():
        raise FileNotFoundError(f"profile photo not found: {candidate}")
    return candidate


def _build_pdfs(paths: BuildPaths, config: ResumeConfig) -> None:
    paths.pdf_dir.mkdir(parents=True, exist_ok=True)
    photo_path = _resolve_photo(paths.project_root, config)
    photo_uri = file_to_data_uri(photo_path) if photo_path is not None else None

    for locale in config.site.languages:
        context = ThemeContext(
            config=config,
            resume=config.data[locale],
            locale=locale,
            project_root=paths.project_root,
            photo_uri=photo_uri,
            web_asset_base="",
        )
        theme = build_theme(config.site.theme.pdf, ThemeOutputType.PDF, context)
        destination = paths.pdf_dir / f"{config.site.output_basename}-{locale.value}.pdf"
        render_pdf(theme, destination)
        _console.print(f"[green]PDF[/green] {destination.relative_to(paths.project_root)}")


def _build_web(paths: BuildPaths, config: ResumeConfig) -> None:
    paths.web_dir.mkdir(parents=True, exist_ok=True)

    if paths.generated_dir.exists():
        shutil.rmtree(paths.generated_dir)
    paths.generated_dir.mkdir(parents=True)

    photo_path = _resolve_photo(paths.project_root, config)
    web_photo_relative: str | None = (
        f"../assets/photo{photo_path.suffix}" if photo_path is not None else None
    )

    # render html into the source folder scanned by tailwind so utilities are detected.
    for locale in config.site.languages:
        context = ThemeContext(
            config=config,
            resume=config.data[locale],
            locale=locale,
            project_root=paths.project_root,
            photo_uri=web_photo_relative,
            web_asset_base="../assets",
        )
        theme = build_theme(config.site.theme.web, ThemeOutputType.WEB, context)
        render_web_html(theme, paths.generated_dir / locale.value / "index.html")

    # vite empties build/web/assets and writes main.css / main.js, so it must run before
    # any other file is placed under that folder.
    _run_vite(paths.frontend_dir)
    paths.web_assets_dir.mkdir(parents=True, exist_ok=True)

    if photo_path is not None:
        shutil.copyfile(photo_path, paths.web_assets_dir / f"photo{photo_path.suffix}")

    for locale in config.site.languages:
        source = paths.generated_dir / locale.value / "index.html"
        target = paths.web_dir / locale.value / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        _console.print(f"[green]HTML[/green] {target.relative_to(paths.project_root)}")

    _write_root_redirect(paths.web_dir / "index.html", config.site.default_language)


def _write_root_redirect(path: Path, default_language: Locale) -> None:
    href = f"./{default_language.value}/index.html"
    html = (
        "<!doctype html>\n"
        f'<meta charset="utf-8">\n<meta http-equiv="refresh" content="0; url={href}">\n'
        f'<link rel="canonical" href="{href}">\n'
        '<link rel="icon" href="./assets/favicon/favicon.ico" sizes="48x48">\n'
        "<title>Redirecting…</title>\n"
        f'<a href="{href}">Continue →</a>\n'
    )
    path.write_text(html, encoding="utf-8")


def _run_vite(frontend_dir: Path) -> None:
    if not (frontend_dir / "node_modules").is_dir():
        _console.print("[cyan]Installing frontend dependencies…[/cyan]")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    _console.print("[cyan]Building frontend assets with Vite…[/cyan]")
    subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
