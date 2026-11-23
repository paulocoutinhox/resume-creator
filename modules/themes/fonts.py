from base64 import b64encode
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FontFace:
    """Single @font-face entry for a font family bundled with a theme."""

    family: str
    weight: int
    style: str
    file: str


def embed_font_faces(faces: tuple[FontFace, ...], font_dir: Path) -> str:
    """Build a CSS string with @font-face rules embedding the given files as data URIs.

    Each file is read from `font_dir`, base64-encoded, and inlined so the resulting
    HTML/CSS is fully self-contained (required for deterministic PDF rendering).
    """
    blocks: list[str] = []
    for face in faces:
        encoded = b64encode((font_dir / face.file).read_bytes()).decode("ascii")
        blocks.append(
            "@font-face{"
            f"font-family:'{face.family}';font-style:{face.style};"
            f"font-weight:{face.weight};font-display:block;"
            f"src:url(data:font/woff2;base64,{encoded}) format('woff2');"
            "}"
        )
    return "".join(blocks)
