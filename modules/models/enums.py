from enum import Enum


class Locale(str, Enum):
    EN = "en"
    PT = "pt"


class ThemeOutputType(str, Enum):
    PDF = "pdf"
    WEB = "web"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Pronouns(str, Enum):
    HE_HIM = "he/him"
    SHE_HER = "she/her"
    THEY_THEM = "they/them"
    CUSTOM = "custom"


class CompanySize(str, Enum):
    SMALL = "small"
    MID = "mid"
    BIG = "big"


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    UNFINISHED_BACHELOR = "unfinished_bachelor"
    TWO_YEAR = "two_year"
    BACHELOR = "bachelor"
    POST_GRADUATION = "post_graduation"
    MBA = "mba"
    MASTER = "master"
    DOCTORAL = "doctoral"
    POST_DOCTORAL = "post_doctoral"


class LanguageLevel(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    UPPER_INTERMEDIATE = "upper_intermediate"
    ADVANCED = "advanced"
    FLUENT = "fluent"
    NATIVE = "native"


class SocialNetwork(str, Enum):
    LINKEDIN = "linkedin"
    GITHUB = "github"
    SITE = "site"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    X = "x"


class IconKey(str, Enum):
    PHONE = "phone"
    WHATSAPP = "whatsapp"
    MAIL = "mail"
    MAP_PIN = "map_pin"
    USER = "user"
    LINKEDIN = "linkedin"
    GITHUB = "github"
    GLOBE = "globe"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    X = "x"
    BRIEFCASE = "briefcase"
    GRADUATION_CAP = "graduation_cap"
    AWARD = "award"
    LANGUAGES = "languages"
    LIGHTBULB = "lightbulb"
    SPARKLES = "sparkles"
    EXTERNAL_LINK = "external_link"
    BUILDING = "building"
    CALENDAR = "calendar"
