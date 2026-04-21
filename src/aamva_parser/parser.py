from __future__ import annotations

from datetime import datetime

from aamva_parser.field_parser import FieldParser
from aamva_parser.license import License
from aamva_parser.regex_util import Regex
from aamva_parser.version_field_parsers import (
    VersionEightFieldParser,
    VersionElevenFieldParser,
    VersionNineFieldParser,
    VersionOneFieldParser,
    VersionSevenFieldParser,
    VersionSixFieldParser,
    VersionTenFieldParser,
    VersionTwelveFieldParser,
    VersionThreeFieldParser,
    VersionTwoFieldParser,
    VersionFourFieldParser,
    VersionFiveFieldParser,
)


class LicenseParser:
    def __init__(self, data: str) -> None:
        self.data = self._clean_and_format_string(data)
        self.field_parser: FieldParser = FieldParser(data)

    def _clean_and_format_string(self, data: str) -> str:
        data = data.replace("\u001e", "").replace("\r", "")
        lines = data.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        data = "\n".join(cleaned_lines)
        if not data.startswith("@"):
            data = "@\n" + data
        return data

    def parse(self) -> License:
        version = self.parse_version()
        self.field_parser = self._version_based_field_parsing(version)

        license_data: dict = {
            "first_name": self.field_parser.parse_first_name(),
            "last_name": self.field_parser.parse_last_name(),
            "middle_name": self.field_parser.parse_middle_name(),
            "expiration_date": self.field_parser.parse_expiration_date(),
            "issue_date": self.field_parser.parse_issue_date(),
            "date_of_birth": self.field_parser.parse_date_of_birth(),
            "gender": self.field_parser.parse_gender(),
            "eye_color": self.field_parser.parse_eye_color(),
            "height": self.field_parser.parse_height(),
            "street_address": self.field_parser.parse_string("street_address"),
            "city": self.field_parser.parse_string("city"),
            "state": self.field_parser.parse_string("state"),
            "postal_code": self.field_parser.parse_string("postal_code"),
            "drivers_license_id": self.field_parser.parse_string("drivers_license_id"),
            "document_id": self.field_parser.parse_string("document_id"),
            "country": self.field_parser.parse_country(),
            "middle_name_truncation": self.field_parser.parse_truncation_status("middle_name_truncation"),
            "first_name_truncation": self.field_parser.parse_truncation_status("first_name_truncation"),
            "last_name_truncation": self.field_parser.parse_truncation_status("last_name_truncation"),
            "street_address_supplement": self.field_parser.parse_string("street_address_supplement"),
            "hair_color": self.field_parser.parse_hair_color(),
            "place_of_birth": self.field_parser.parse_string("place_of_birth"),
            "audit_information": self.field_parser.parse_string("audit_information"),
            "inventory_control_number": self.field_parser.parse_string("inventory_control_number"),
            "last_name_alias": self.field_parser.parse_string("last_name_alias"),
            "first_name_alias": self.field_parser.parse_string("first_name_alias"),
            "suffix_alias": self.field_parser.parse_string("suffix_alias"),
            "suffix": self.field_parser.parse_name_suffix(),
            "version": version,
            "pdf417": self.data,
            "expired": self.field_parser.parse_is_expired(),
            "weight": self.field_parser.parse_string("weight"),
            "cdl_indicator": self.field_parser.parse_string("cdl_indicator"),
            "non_domiciled_indicator": self.field_parser.parse_string("non_domiciled_indicator"),
            "enhanced_credential_indicator": self.field_parser.parse_string("enhanced_credential_indicator"),
            "permit_indicator": self.field_parser.parse_string("permit_indicator"),
        }

        return License.from_dict(license_data)

    def parse_version(self) -> str | None:
        return Regex().first_match(r"\d{6}(\d{2})\w+", self.data)

    def _version_based_field_parsing(self, version: str | None) -> FieldParser:
        default_parser = FieldParser(self.data)

        if not version:
            return default_parser

        parsers: dict[str, type[FieldParser]] = {
            "01": VersionOneFieldParser,
            "02": VersionTwoFieldParser,
            "03": VersionThreeFieldParser,
            "04": VersionFourFieldParser,
            "05": VersionFiveFieldParser,
            "06": VersionSixFieldParser,
            "07": VersionSevenFieldParser,
            "08": VersionEightFieldParser,
            "09": VersionNineFieldParser,
            "10": VersionTenFieldParser,
            "11": VersionElevenFieldParser,
            "12": VersionTwelveFieldParser,
        }
        parser_cls = parsers.get(version)
        return parser_cls(self.data) if parser_cls else default_parser

    def is_expired(self) -> bool:
        expiration_date = self.field_parser.parse_expiration_date()
        return expiration_date is not None and datetime.now() > expiration_date
