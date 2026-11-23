from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from rich.console import Console


_console = Console()


def run_serve(web_dir: Path, host: str, port: int) -> None:
    if not web_dir.is_dir():
        raise FileNotFoundError(f"web build directory not found: {web_dir}. run `python main.py build web` first.")
    handler = partial(SimpleHTTPRequestHandler, directory=str(web_dir))
    server = ThreadingHTTPServer((host, port), handler)
    _console.print(f"[cyan]Serving[/cyan] {web_dir} at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _console.print("[yellow]Shutting down…[/yellow]")
    finally:
        server.server_close()
