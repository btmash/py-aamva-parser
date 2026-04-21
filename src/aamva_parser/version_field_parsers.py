from __future__ import annotations

from aamva_parser.enums import NameSuffix
from aamva_parser.field_parser import FieldParser, suffix_to_enum
from aamva_parser.version_mappers import (
    VersionEightFieldMapper,
    VersionElevenFieldMapper,
    VersionFiveFieldMapper,
    VersionFourFieldMapper,
    VersionNineFieldMapper,
    VersionOneFieldMapper,
    VersionSevenFieldMapper,
    VersionSixFieldMapper,
    VersionTenFieldMapper,
    VersionThreeFieldMapper,
    VersionTwelveFieldMapper,
    VersionTwoFieldMapper,
)


class VersionOneFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionOneFieldMapper())

    def parse_first_name(self) -> str | None:
        first_name = self.parse_string("first_name")
        return first_name or self._parse_driver_license_name("first_name")

    def parse_last_name(self) -> str | None:
        last_name = self.parse_string("last_name")
        return last_name or self._parse_driver_license_name("last_name")

    def parse_middle_name(self) -> str | None:
        middle_name = self.parse_string("middle_name")
        return middle_name or self._parse_driver_license_name("middle_name")

    def parse_height(self) -> float | None:
        height_in_feet_and_inches = self.parse_string("height")
        if not height_in_feet_and_inches:
            return None

        height = self.regex.first_match(r"([0-9]{1})", height_in_feet_and_inches)
        inches = self.regex.first_match(r"[0-9]{1}([0-9]{2})", height_in_feet_and_inches)

        if not height or not inches:
            return None

        calculated_height = (float(height) * 12) + float(inches)

        if "cm" in height_in_feet_and_inches.lower():
            return round(calculated_height * self.INCHES_PER_CENTIMETER)
        return calculated_height

    def parse_name_suffix(self) -> NameSuffix:
        suffix = self.parse_string("suffix") or self._parse_driver_license_name("suffix")
        return suffix_to_enum(suffix)

    def _parse_driver_license_name(self, key: str) -> str | None:
        driver_license_name = self.parse_string("driver_license_name")
        if not driver_license_name:
            return None

        name_pieces = driver_license_name.split(",")
        if key == "last_name":
            return name_pieces[0].strip() if name_pieces else None
        if key == "first_name":
            return name_pieces[1].strip() if len(name_pieces) > 1 else None
        if key == "middle_name":
            return name_pieces[2].strip() if len(name_pieces) > 2 else None
        if key == "suffix":
            return name_pieces[3].strip() if len(name_pieces) > 3 else None
        return None


class VersionTwoFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionTwoFieldMapper())


class VersionThreeFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionThreeFieldMapper())


class VersionFourFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionFourFieldMapper())


class VersionFiveFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionFiveFieldMapper())


class VersionSixFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionSixFieldMapper())


class VersionSevenFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionSevenFieldMapper())


class VersionEightFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionEightFieldMapper())


class VersionNineFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionNineFieldMapper())


class VersionTenFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionTenFieldMapper())


class VersionElevenFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionElevenFieldMapper())


class VersionTwelveFieldParser(FieldParser):
    def __init__(self, data: str) -> None:
        super().__init__(data, VersionTwelveFieldMapper())
