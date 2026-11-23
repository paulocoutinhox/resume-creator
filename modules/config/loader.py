from pathlib import Path
from typing import Any

import yaml

from modules.models.enums import ThemeOutputType
from modules.models.resume import ResumeConfig
from modules.themes.registry import ThemeOutputMismatchError, UnknownThemeError, ensure_theme_registered


class ConfigLoadError(RuntimeError):
    pass


def load_config(path: Path) -> ResumeConfig:
    if not path.is_file():
        raise ConfigLoadError(f"config file not found: {path}")
    raw = _read_yaml_mapping(path)
    raw["data"] = _resolve_data_block(raw.get("data"), path.parent)
    config = ResumeConfig.model_validate(raw)
    try:
        ensure_theme_registered(config.site.theme.pdf, ThemeOutputType.PDF)
        ensure_theme_registered(config.site.theme.web, ThemeOutputType.WEB)
    except (UnknownThemeError, ThemeOutputMismatchError) as exc:
        raise ConfigLoadError(str(exc)) from exc
    return config


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ConfigLoadError(f"yaml root must be a mapping at {path}, got {type(data).__name__}")
    return data


def _resolve_data_block(value: Any, base_dir: Path) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigLoadError("config 'data' must be a mapping of locale → file path or inline block")
    resolved: dict[str, Any] = {}
    for locale_key, entry in value.items():
        if isinstance(entry, str):
            target = (base_dir / entry).resolve()
            resolved[locale_key] = _read_yaml_mapping(target)
            continue
        if isinstance(entry, dict):
            resolved[locale_key] = entry
            continue
        raise ConfigLoadError(
            f"data['{locale_key}'] must be a file path or an inline mapping, got {type(entry).__name__}"
        )
    return resolved
