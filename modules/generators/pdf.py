from pathlib import Path

from weasyprint import HTML

from modules.themes.base import Theme


def render_pdf(theme: Theme, destination: Path) -> Path:
    html_text = theme.render()
    destination.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_text, base_url=str(theme.context.project_root)).write_pdf(target=str(destination))
    return destination
