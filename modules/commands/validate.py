from pathlib import Path

from rich.console import Console
from rich.table import Table

from modules.config.loader import load_config


_console = Console()


def run_validate(config_path: Path) -> None:
    config = load_config(config_path)
    table = Table(title="Resume configuration", show_header=True, header_style="bold")
    table.add_column("Locale")
    table.add_column("Sections")
    for locale in config.site.languages:
        block = config.data[locale]
        sections = [
            f"experience:{len(block.experience)}",
            f"education:{len(block.education)}",
            f"certifications:{len(block.certifications)}",
            f"side_projects:{len(block.side_projects)}",
            f"open_source_projects:{len(block.open_source_projects)}",
            f"languages:{len(block.languages)}",
            f"social:{len(block.social)}",
        ]
        table.add_row(locale.value, ", ".join(sections))
    _console.print(table)
    _console.print(
        f"[green]OK[/green] theme.pdf={config.site.theme.pdf} theme.web={config.site.theme.web} "
        f"default={config.site.default_language.value}"
    )
