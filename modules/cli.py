from pathlib import Path

import click

from modules.commands.build import run_build
from modules.commands.serve import run_serve
from modules.commands.validate import run_validate


_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CONFIG = _PROJECT_ROOT / "data" / "config.yml"


def _config_option():
    return click.option(
        "--config",
        "config_path",
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        default=_DEFAULT_CONFIG,
        show_default=True,
        help="Path to the resume YAML configuration.",
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """Resume creator command line interface."""


@cli.group(invoke_without_command=True)
@_config_option()
@click.pass_context
def build(ctx: click.Context, config_path: Path) -> None:
    """Build PDF and web outputs (default action)."""
    if ctx.invoked_subcommand is None:
        run_build(_PROJECT_ROOT, config_path, targets=("pdf", "web"))


@build.command("pdf")
@_config_option()
def build_pdf(config_path: Path) -> None:
    """Build PDF outputs only."""
    run_build(_PROJECT_ROOT, config_path, targets=("pdf",))


@build.command("web")
@_config_option()
def build_web(config_path: Path) -> None:
    """Build the web (Vite + Tailwind) output only."""
    run_build(_PROJECT_ROOT, config_path, targets=("web",))


@cli.command()
@_config_option()
def validate(config_path: Path) -> None:
    """Validate the configuration file."""
    run_validate(config_path)


@cli.command()
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=4173, show_default=True, type=int)
def serve(host: str, port: int) -> None:
    """Serve the build/web folder locally for preview."""
    run_serve(_PROJECT_ROOT / "build" / "web", host, port)
