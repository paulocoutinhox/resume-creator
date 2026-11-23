from datetime import date

from modules.i18n.translator import Translator
from modules.models.resume import MonthDate


def months_between(start: MonthDate, end: MonthDate | None) -> int:
    """Number of full months from start (inclusive) to end (inclusive)."""

    end_date = end.to_date() if end is not None else date.today().replace(day=1)
    start_date = start.to_date()
    if end_date < start_date:
        raise ValueError("end date is before start date")
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1


def humanize_duration(months: int, translator: Translator) -> str:
    if months <= 0:
        raise ValueError("duration must be positive")
    if months < 12:
        key = "duration.month_one" if months == 1 else "duration.month_other"
        return translator.t(key, count=months)
    years = months // 12
    remaining = months % 12
    year_key = "duration.year_one" if years == 1 else "duration.year_other"
    years_text = translator.t(year_key, count=years)
    if remaining == 0:
        return years_text
    month_key = "duration.month_one" if remaining == 1 else "duration.month_other"
    months_text = translator.t(month_key, count=remaining)
    return translator.t("duration.year_and_month", years=years_text, months=months_text)
