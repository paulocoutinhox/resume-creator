from pathlib import Path

from modules.themes.base import Theme


def render_web_html(theme: Theme, destination: Path) -> Path:
    html_text = theme.render()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html_text, encoding="utf-8")
    return destination
