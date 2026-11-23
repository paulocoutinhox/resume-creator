from pathlib import Path

from modules.models.enums import ThemeOutputType
from modules.themes.base import Theme
from modules.themes.fonts import FontFace, embed_font_faces


_THEME_ROOT = Path(__file__).resolve().parent
_FONT_DIR = _THEME_ROOT / "fonts"

# fonts bundled with this theme. to swap the typography:
#   1. drop the new .woff2 files into modules/themes/modern_pdf/fonts/
#   2. update the entries below (family + weight + style + filename)
#   3. update the `font-family` declaration in styles/pdf.css
# every face listed here is embedded into the rendered html as a data uri,
# so the resulting pdf is self-contained and renders identically on any host.
FONT_FAMILY = "Roboto"
FONT_FACES: tuple[FontFace, ...] = (
    FontFace(FONT_FAMILY, 400, "normal", "Roboto-Regular.woff2"),
    FontFace(FONT_FAMILY, 400, "italic", "Roboto-Italic.woff2"),
    FontFace(FONT_FAMILY, 700, "normal", "Roboto-Bold.woff2"),
    FontFace(FONT_FAMILY, 700, "italic", "Roboto-BoldItalic.woff2"),
)


class ModernPdfTheme(Theme):
    name = "modern-pdf"
    output_type = ThemeOutputType.PDF

    @property
    def template_root(self) -> Path:
        return _THEME_ROOT / "templates"

    def render(self) -> str:
        stylesheet = embed_font_faces(FONT_FACES, _FONT_DIR) + (
            _THEME_ROOT / "styles" / "pdf.css"
        ).read_text(encoding="utf-8")
        template = self.env.get_template("layout.html")
        return template.render(
            resume=self.context.resume,
            site=self.context.config.site,
            stylesheet=stylesheet,
        )
