from __future__ import annotations

from datetime import date

from aamva_parser.enums import EyeColor, Gender, HairColor, IssuingCountry, NameSuffix, Truncation
from aamva_parser.license import License
from aamva_parser.parser import LicenseParser

__all__ = [
    "License",
    "LicenseParser",
    "parse",
    "get_version",
    "is_expired",
    "get_age",
    "is_under_21",
    "is_under_18",
    "is_acceptable",
    "get_full_name",
    "get_state",
    "is_cdl",
    "Gender",
    "EyeColor",
    "HairColor",
    "IssuingCountry",
    "Truncation",
    "NameSuffix",
    "Parse",
    "GetVersion",
    "IsExpired",
]


def parse(barcode: str) -> License:
    return LicenseParser(barcode).parse()


def get_version(barcode: str) -> str | None:
    return LicenseParser(barcode).parse_version()


def is_expired(barcode: str) -> bool:
    return LicenseParser(barcode).is_expired()


def get_age(barcode: str) -> int | None:
    lic = parse(barcode)
    if lic.date_of_birth is None:
        return None
    today = date.today()
    dob = lic.date_of_birth.date()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


def is_under_21(barcode: str) -> bool:
    age = get_age(barcode)
    return age is not None and age < 21


def is_under_18(barcode: str) -> bool:
    age = get_age(barcode)
    return age is not None and age < 18


def is_acceptable(barcode: str) -> bool:
    return parse(barcode).is_acceptable()


def get_full_name(barcode: str) -> str | None:
    lic = parse(barcode)
    parts = [p for p in (lic.first_name, lic.middle_name, lic.last_name) if p]
    return " ".join(parts) if parts else None


def get_state(barcode: str) -> str | None:
    return parse(barcode).state


def is_cdl(barcode: str) -> bool:
    return parse(barcode).cdl_indicator == "1"


def Parse(barcode: str) -> License:
    return parse(barcode)


def GetVersion(barcode: str) -> str | None:
    return get_version(barcode)


def IsExpired(barcode: str) -> bool:
    return is_expired(barcode)
