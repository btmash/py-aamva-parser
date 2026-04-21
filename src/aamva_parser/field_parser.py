from __future__ import annotations

from datetime import datetime
from re import escape as re_escape

from aamva_parser.enums import (
    EyeColor,
    Gender,
    HairColor,
    IssuingCountry,
    NameSuffix,
    Truncation,
)
from aamva_parser.field_mapping import FieldMapper, FieldMapping
from aamva_parser.regex_util import Regex


class FieldParser:
    INCHES_PER_CENTIMETER: float = 0.393701

    def __init__(self, data: str, field_mapper: FieldMapping | None = None) -> None:
        self.data = data
        self.field_mapper = field_mapper if field_mapper is not None else FieldMapper()
        self.regex = Regex()

    def parse_string(self, key: str) -> str | None:
        identifier = self.field_mapper.field_for(key)
        return self.regex.first_match(rf"{re_escape_identifier(identifier)}(.+)\b", self.data)

    def parse_double(self, key: str) -> float | None:
        identifier = self.field_mapper.field_for(key)
        result = self.regex.first_match(rf"{re_escape_identifier(identifier)}(\w+)\b", self.data)
        return float(result) if result is not None else None

    def parse_date(self, field: str) -> datetime | None:
        date_string = self.parse_string(field)
        if not date_string or len(date_string) != 8:
            return None

        month = int(date_string[0:2])
        day = int(date_string[2:4])
        year = int(date_string[4:8])

        try:
            return datetime(year, month, day)
        except ValueError:
            return None

    def parse_first_name(self) -> str | None:
        return self.parse_string("first_name")

    def parse_last_name(self) -> str | None:
        return self.parse_string("last_name")

    def parse_middle_name(self) -> str | None:
        return self.parse_string("middle_name")

    def parse_expiration_date(self) -> datetime | None:
        return self.parse_date("expiration_date")

    def parse_is_expired(self) -> bool:
        expiration_date = self.parse_expiration_date()
        return expiration_date is not None and datetime.now() > expiration_date

    def parse_issue_date(self) -> datetime | None:
        return self.parse_date("issue_date")

    def parse_date_of_birth(self) -> datetime | None:
        return self.parse_date("date_of_birth")

    def parse_country(self) -> IssuingCountry:
        country = self.parse_string("country")
        if country == "USA":
            return IssuingCountry.UNITED_STATES
        if country == "CAN":
            return IssuingCountry.CANADA
        return IssuingCountry.UNKNOWN

    def parse_truncation_status(self, field: str) -> Truncation:
        truncation = self.parse_string(field)
        if truncation == "T":
            return Truncation.TRUNCATED
        if truncation == "N":
            return Truncation.NONE
        return Truncation.UNKNOWN

    def parse_gender(self) -> Gender:
        gender = self.parse_string("gender")
        if gender == "1":
            return Gender.MALE
        if gender == "2":
            return Gender.FEMALE
        return Gender.OTHER

    def parse_eye_color(self) -> EyeColor:
        color = self.parse_string("eye_color")
        mapping = {
            "BLK": EyeColor.BLACK,
            "BLU": EyeColor.BLUE,
            "BRO": EyeColor.BROWN,
            "GRY": EyeColor.GRAY,
            "GRN": EyeColor.GREEN,
            "HAZ": EyeColor.HAZEL,
            "MAR": EyeColor.MAROON,
            "PNK": EyeColor.PINK,
            "DIC": EyeColor.DICHROMATIC,
        }
        return mapping.get(color or "", EyeColor.UNKNOWN)

    def parse_name_suffix(self) -> NameSuffix:
        suffix = self.parse_string("suffix")
        return suffix_to_enum(suffix)

    def parse_hair_color(self) -> HairColor:
        color = self.parse_string("hair_color")
        mapping = {
            "BAL": HairColor.BALD,
            "BLK": HairColor.BLACK,
            "BLN": HairColor.BLOND,
            "BRO": HairColor.BROWN,
            "GRY": HairColor.GREY,
            "RED": HairColor.RED,
            "SDY": HairColor.SANDY,
            "WHI": HairColor.WHITE,
        }
        return mapping.get(color or "", HairColor.UNKNOWN)

    def parse_height(self) -> float | None:
        height_string = self.parse_string("height")
        height = self.parse_double("height")
        if not height_string or height is None:
            return None

        if "cm" in height_string.lower():
            return round(height * self.INCHES_PER_CENTIMETER)
        return height


def re_escape_identifier(identifier: str) -> str:
    """AAMVA identifiers are alphanumeric; escape for regex safety."""
    return re_escape(identifier)


def suffix_to_enum(suffix: str | None) -> NameSuffix:
    if not suffix:
        return NameSuffix.UNKNOWN
    table = {
        "JR": NameSuffix.JUNIOR,
        "SR": NameSuffix.SENIOR,
        "1ST": NameSuffix.FIRST,
        "I": NameSuffix.FIRST,
        "2ND": NameSuffix.SECOND,
        "II": NameSuffix.SECOND,
        "3RD": NameSuffix.THIRD,
        "III": NameSuffix.THIRD,
        "4TH": NameSuffix.FOURTH,
        "IV": NameSuffix.FOURTH,
        "5TH": NameSuffix.FIFTH,
        "V": NameSuffix.FIFTH,
        "6TH": NameSuffix.SIXTH,
        "VI": NameSuffix.SIXTH,
        "7TH": NameSuffix.SEVENTH,
        "VII": NameSuffix.SEVENTH,
        "8TH": NameSuffix.EIGHTH,
        "VIII": NameSuffix.EIGHTH,
        "9TH": NameSuffix.NINTH,
        "IX": NameSuffix.NINTH,
    }
    return table.get(suffix.upper(), NameSuffix.UNKNOWN)
