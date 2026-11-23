from pathlib import Path
from typing import Any

import yaml

from modules.models.enums import Locale


_LOCALES_DIR = Path(__file__).resolve().parent / "locales"


class TranslationError(KeyError):
    pass


class Translator:
    def __init__(self, locale: Locale) -> None:
        self._locale = locale
        self._catalog = self._load(locale)

    @property
    def locale(self) -> Locale:
        return self._locale

    @staticmethod
    def _load(locale: Locale) -> dict[str, str]:
        path = _LOCALES_DIR / f"{locale.value}.yml"
        if not path.is_file():
            raise TranslationError(f"locale catalog not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if not isinstance(data, dict):
            raise TranslationError(f"locale catalog root must be a mapping: {path}")
        return _flatten(data)

    def t(self, key: str, **kwargs: Any) -> str:
        if key not in self._catalog:
            raise TranslationError(f"missing translation key '{key}' for locale '{self._locale.value}'")
        template = self._catalog[key]
        if not kwargs:
            return template
        return template.format(**kwargs)


def _flatten(data: dict[str, Any], prefix: str = "") -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in data.items():
        composite = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(_flatten(value, composite))
            continue
        if not isinstance(value, str):
            raise TranslationError(f"locale value for '{composite}' must be a string")
        result[composite] = value
    return result
