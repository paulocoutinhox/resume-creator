from abc import ABC, abstractmethod
from base64 import b64encode
from dataclasses import dataclass
from mimetypes import guess_type
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from modules.i18n.translator import Translator
from modules.models.enums import IconKey, Locale, ThemeOutputType
from modules.models.resume import LocalizedResume, ResumeConfig
from modules.themes.icons import render_icon, social_icon_key
from modules.utils.dates import format_birth_date, format_month_year
from modules.utils.duration import humanize_duration, months_between


@dataclass(frozen=True)
class ThemeContext:
    config: ResumeConfig
    resume: LocalizedResume
    locale: Locale
    project_root: Path
    photo_uri: str | None
    web_asset_base: str


class Theme(ABC):
    name: str
    output_type: ThemeOutputType

    def __init__(self, context: ThemeContext) -> None:
        self.context = context
        self.translator = Translator(context.locale)
        self.env = self._build_env()
        self._register_globals()

    def _build_env(self) -> Environment:
        loader = FileSystemLoader(str(self.template_root))
        return Environment(
            loader=loader,
            autoescape=select_autoescape(enabled_extensions=("html",)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _register_globals(self) -> None:
        self.env.globals["t"] = self.translator.t
        self.env.globals["icon"] = render_icon
        self.env.globals["IconKey"] = IconKey
        self.env.globals["social_icon_key"] = social_icon_key
        self.env.globals["format_month_year"] = lambda value: format_month_year(value, self.context.locale)
        self.env.globals["format_birth_date"] = lambda value: format_birth_date(value, self.context.locale)
        self.env.globals["humanize_duration"] = lambda months: humanize_duration(months, self.translator)
        self.env.globals["months_between"] = months_between
        self.env.globals["photo_uri"] = self.context.photo_uri
        self.env.globals["web_asset_base"] = self.context.web_asset_base

    @property
    @abstractmethod
    def template_root(self) -> Path:
        ...

    @abstractmethod
    def render(self) -> str:
        ...


def file_to_data_uri(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"asset not found: {path}")
    mime, _ = guess_type(path.name)
    if mime is None:
        raise ValueError(f"unknown mime type for asset: {path}")
    encoded = b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"
