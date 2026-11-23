from pathlib import Path

from modules.models.enums import ThemeOutputType
from modules.themes.base import Theme


_THEME_ROOT = Path(__file__).resolve().parent


class ModernWebTheme(Theme):
    name = "modern-web"
    output_type = ThemeOutputType.WEB

    @property
    def template_root(self) -> Path:
        return _THEME_ROOT / "templates"

    def render(self) -> str:
        template = self.env.get_template("layout.html")
        return template.render(
            resume=self.context.resume,
            site=self.context.config.site,
            locale=self.context.locale,
        )
