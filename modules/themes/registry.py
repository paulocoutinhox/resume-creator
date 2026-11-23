from modules.models.enums import ThemeOutputType
from modules.themes.base import Theme, ThemeContext
from modules.themes.modern_web.theme import ModernWebTheme
from modules.themes.modern_pdf.theme import ModernPdfTheme


_THEMES: dict[str, type[Theme]] = {
    ModernPdfTheme.name: ModernPdfTheme,
    ModernWebTheme.name: ModernWebTheme,
}


class UnknownThemeError(KeyError):
    pass


class ThemeOutputMismatchError(ValueError):
    pass


def _theme_class(name: str, output_type: ThemeOutputType) -> type[Theme]:
    if name not in _THEMES:
        available = ", ".join(sorted(_THEMES))
        raise UnknownThemeError(f"unknown theme '{name}'. available: {available}")
    theme_cls = _THEMES[name]
    if theme_cls.output_type is not output_type:
        raise ThemeOutputMismatchError(
            f"theme '{name}' targets {theme_cls.output_type.value}, but {output_type.value} was requested"
        )
    return theme_cls


def ensure_theme_registered(name: str, output_type: ThemeOutputType) -> None:
    """Fail fast when config references an unknown theme or the wrong output type."""
    _theme_class(name, output_type)


def build_theme(name: str, output_type: ThemeOutputType, context: ThemeContext) -> Theme:
    return _theme_class(name, output_type)(context)
