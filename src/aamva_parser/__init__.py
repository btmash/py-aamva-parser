from __future__ import annotations

from datetime import date
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _distribution_version

from aamva_parser.enums import (
    EyeColor,
    Gender,
    HairColor,
    IssuingCountry,
    NameSuffix,
    Truncation,
)
from aamva_parser.license import License
from aamva_parser.parsed_license import ParsedLicense
from aamva_parser.parser import LicenseParser

__all__ = [
    "EyeColor",
    "Gender",
    "GetVersion",
    "HairColor",
    "IsExpired",
    "IssuingCountry",
    "License",
    "LicenseParser",
    "NameSuffix",
    "Parse",
    "ParsedLicense",
    "Truncation",
    "__version__",
    "get_age",
    "get_full_name",
    "get_state",
    "get_version",
    "is_acceptable",
    "is_cdl",
    "is_expired",
    "is_under_18",
    "is_under_21",
    "parse",
]


def parse(barcode: str) -> ParsedLicense:
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
    s = parse(barcode).state
    return s if s else None


def is_cdl(barcode: str) -> bool:
    return parse(barcode).cdl_indicator == "1"


# Deprecated PascalCase aliases (JavaScript parity); prefer snake_case above.
from aamva_parser.compat import GetVersion, IsExpired, Parse

try:
    __version__: str = _distribution_version("aamva-parser")
except PackageNotFoundError:
    # Editable checkout without metadata, or tests on PYTHONPATH without install.
    __version__ = "0.dev0"
