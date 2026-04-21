from __future__ import annotations

from aamva_parser.field_mapping import FieldMapper


def _base_fields() -> dict[str, str]:
    return FieldMapper().copy_fields()


class VersionOneFieldMapper:
    def __init__(self) -> None:
        self.fields = _base_fields()
        self.fields["drivers_license_id"] = "DBJ"
        self.fields["last_name"] = "DAB"
        self.fields["driver_license_name"] = "DAA"

    def field_for(self, key: str) -> str:
        return self.fields.get(key) or key


class VersionTwoFieldMapper:
    def __init__(self) -> None:
        self.fields = _base_fields()
        self.fields["first_name"] = "DCT"

    def field_for(self, key: str) -> str:
        return self.fields.get(key) or key


class VersionThreeFieldMapper(VersionTwoFieldMapper):
    pass


class VersionFourFieldMapper:
    def __init__(self) -> None:
        self.fields = _base_fields()

    def field_for(self, key: str) -> str:
        return self.fields.get(key) or key


class VersionFiveFieldMapper(VersionFourFieldMapper):
    pass


class VersionSixFieldMapper(VersionFourFieldMapper):
    pass


class VersionSevenFieldMapper(VersionFourFieldMapper):
    pass


class VersionEightFieldMapper(VersionFourFieldMapper):
    pass


class VersionNineFieldMapper(VersionFourFieldMapper):
    pass


class VersionTenFieldMapper(VersionFourFieldMapper):
    pass


class VersionElevenFieldMapper(VersionFourFieldMapper):
    pass


class VersionTwelveFieldMapper:
    def __init__(self) -> None:
        self.fields = {
            **_base_fields(),
            "cdl_indicator": "DDM",
            "non_domiciled_indicator": "DDN",
            "enhanced_credential_indicator": "DDO",
            "permit_indicator": "DDP",
        }
        self.fields.pop("last_name_alias", None)
        self.fields.pop("first_name_alias", None)
        self.fields.pop("suffix_alias", None)

    def field_for(self, key: str) -> str:
        return self.fields.get(key) or key
