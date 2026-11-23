from datetime import date
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from modules.models.enums import (
    CompanySize,
    EducationLevel,
    LanguageLevel,
    Locale,
    Pronouns,
    Gender,
    SocialNetwork,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=True)


class MonthDate(StrictModel):
    """Year/month value used by experience, education, certifications and side projects."""

    year: Annotated[int, Field(ge=1900, le=2100)]
    month: Annotated[int, Field(ge=1, le=12)]

    def to_date(self) -> date:
        return date(self.year, self.month, 1)


PresentOr = MonthDate | None


class BirthDate(StrictModel):
    """Optional birth date. The day is optional so candidates may share only the
    birth month/year if they prefer not to expose the exact day."""

    year: Annotated[int, Field(ge=1900, le=2100)]
    month: Annotated[int, Field(ge=1, le=12)]
    day: Annotated[int, Field(ge=1, le=31)] | None = None

    @field_validator("day")
    @classmethod
    def _day_matches_month(cls, value: int | None, info) -> int | None:
        if value is None:
            return value
        year = info.data.get("year")
        month = info.data.get("month")
        if year is None or month is None:
            return value
        try:
            date(year, month, value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        return value


class Profile(StrictModel):
    name: str
    email: str
    phone: str | None = None
    whatsapp: str | None = None
    location: str | None = None
    citizenship: str | None = None
    gender: Gender | None = None
    pronouns: Pronouns | None = None
    pronouns_custom: str | None = None
    birth: BirthDate | None = None

    @field_validator("pronouns_custom")
    @classmethod
    def _custom_requires_custom_enum(cls, value: str | None, info) -> str | None:
        pronouns = info.data.get("pronouns")
        if value is not None and pronouns is not Pronouns.CUSTOM:
            raise ValueError("pronouns_custom is only valid when pronouns is 'custom'")
        if value is None and pronouns is Pronouns.CUSTOM:
            raise ValueError("pronouns_custom is required when pronouns is 'custom'")
        return value


class Professional(StrictModel):
    role: str
    role_start: MonthDate
    summary: str
    top_skills: list[str] = Field(min_length=1)
    skills: list[str] = Field(default_factory=list)


class SocialLink(StrictModel):
    network: SocialNetwork
    url: HttpUrl
    handle: str | None = None


class LanguageEntry(StrictModel):
    name: str
    level: LanguageLevel


class Experience(StrictModel):
    company: str
    location: str | None = None
    company_size: CompanySize | None = None
    role: str
    start: MonthDate
    end: PresentOr = None
    description: str | None = None
    bullets: list[str] = Field(default_factory=list)


class Education(StrictModel):
    level: EducationLevel
    institution: str
    title: str
    start: MonthDate
    end: PresentOr = None
    description: str | None = None
    bullets: list[str] = Field(default_factory=list)


class Certification(StrictModel):
    institution: str
    title: str
    start: MonthDate
    end: PresentOr = None
    credential_url: HttpUrl | None = None
    bullets: list[str] = Field(default_factory=list)


class SideProject(StrictModel):
    title: str
    description: str
    url: HttpUrl | None = None
    start: MonthDate
    end: PresentOr = None
    bullets: list[str] = Field(default_factory=list)


class OpenSourceProject(StrictModel):
    title: str
    description: str
    url: HttpUrl | None = None
    start: MonthDate
    end: PresentOr = None
    bullets: list[str] = Field(default_factory=list)


class LocalizedResume(StrictModel):
    profile: Profile
    professional: Professional
    social: list[SocialLink] = Field(default_factory=list)
    languages: list[LanguageEntry] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    side_projects: list[SideProject] = Field(default_factory=list)
    open_source_projects: list[OpenSourceProject] = Field(default_factory=list)


class ThemeSelection(StrictModel):
    pdf: str
    web: str


class SiteConfig(StrictModel):
    languages: list[Locale] = Field(min_length=1)
    default_language: Locale
    output_basename: str = "resume"
    theme: ThemeSelection

    @field_validator("default_language")
    @classmethod
    def _default_must_be_in_languages(cls, value: Locale, info) -> Locale:
        languages = info.data.get("languages")
        if languages is not None and value not in languages:
            raise ValueError("default_language must be present in languages")
        return value


class Assets(StrictModel):
    photo: Path | None = None


class ResumeConfig(StrictModel):
    site: SiteConfig
    assets: Assets = Field(default_factory=Assets)
    data: dict[Locale, LocalizedResume]

    @field_validator("data")
    @classmethod
    def _data_covers_languages(
        cls, value: dict[Locale, LocalizedResume], info
    ) -> dict[Locale, LocalizedResume]:
        site: SiteConfig | None = info.data.get("site")
        if site is None:
            return value
        missing = [lang.value for lang in site.languages if lang not in value]
        if missing:
            raise ValueError(f"missing data block(s) for language(s): {', '.join(missing)}")
        return value
