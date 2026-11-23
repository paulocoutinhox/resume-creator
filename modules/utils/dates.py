from datetime import date

from babel.dates import format_date as babel_format_date

from modules.models.enums import Locale
from modules.models.resume import BirthDate, MonthDate


_BABEL_LOCALE: dict[Locale, str] = {
    Locale.EN: "en_US",
    Locale.PT: "pt_BR",
}


def format_month_year(value: MonthDate, locale: Locale) -> str:
    return babel_format_date(value.to_date(), format="MMM y", locale=_BABEL_LOCALE[locale]).title()


def format_birth_date(value: BirthDate, locale: Locale) -> str:
    """Render a BirthDate. With day → 'd MMMM y' (locale aware); without day → 'MMMM y'."""
    babel_locale = _BABEL_LOCALE[locale]
    if value.day is None:
        return babel_format_date(date(value.year, value.month, 1), format="MMMM y", locale=babel_locale).title()
    return babel_format_date(date(value.year, value.month, value.day), format="d MMMM y", locale=babel_locale)
