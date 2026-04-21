from datetime import datetime

from aamva_parser.enums import (
    EyeColor,
    Gender,
    HairColor,
    IssuingCountry,
    NameSuffix,
    Truncation,
)
from aamva_parser.license import License


def test_empty_license_defaults() -> None:
    lic = License()
    assert lic.first_name is None
    assert lic.last_name is None
    assert lic.middle_name is None
    assert lic.expiration_date is None
    assert lic.issue_date is None
    assert lic.date_of_birth is None
    assert lic.gender is Gender.UNKNOWN
    assert lic.eye_color is EyeColor.UNKNOWN
    assert lic.height is None
    assert lic.street_address is None
    assert lic.city is None
    assert lic.state is None
    assert lic.postal_code is None
    assert lic.drivers_license_id is None
    assert lic.document_id is None
    assert lic.country is IssuingCountry.UNKNOWN
    assert lic.middle_name_truncation is Truncation.NONE
    assert lic.first_name_truncation is Truncation.NONE
    assert lic.last_name_truncation is Truncation.NONE
    assert lic.street_address_supplement is None
    assert lic.hair_color is HairColor.UNKNOWN
    assert lic.place_of_birth is None
    assert lic.audit_information is None
    assert lic.inventory_control_number is None
    assert lic.last_name_alias is None
    assert lic.first_name_alias is None
    assert lic.suffix_alias is None
    assert lic.suffix is NameSuffix.UNKNOWN
    assert lic.version is None
    assert lic.pdf417 is None


def test_is_expired() -> None:
    assert License(expiration_date=datetime(2000, 1, 1)).is_expired() is True
    assert License(expiration_date=datetime(2099, 1, 1)).is_expired() is False


def test_has_been_issued() -> None:
    assert License(issue_date=datetime(2000, 1, 1)).has_been_issued() is True
    assert License(issue_date=datetime(2099, 1, 1)).has_been_issued() is False


def test_is_acceptable() -> None:
    acceptable = License(
        expiration_date=datetime(2099, 1, 1),
        issue_date=datetime(2000, 1, 1),
        last_name="Doe",
        first_name="John",
        middle_name="A",
        date_of_birth=datetime(1980, 1, 1),
        height=180,
        street_address="123 Main St",
        city="Springfield",
        state="IL",
        postal_code="62704",
        document_id="123456789",
    )
    assert acceptable.is_acceptable() is True
    assert License().is_acceptable() is False


def test_cds_2025_fields() -> None:
    lic = License(
        cdl_indicator="1",
        non_domiciled_indicator="1",
        enhanced_credential_indicator="1",
        permit_indicator="1",
    )
    assert lic.cdl_indicator == "1"
    assert lic.non_domiciled_indicator == "1"
    assert lic.enhanced_credential_indicator == "1"
    assert lic.permit_indicator == "1"


def test_cds_defaults_null() -> None:
    lic = License()
    assert lic.cdl_indicator is None
    assert lic.non_domiciled_indicator is None
    assert lic.enhanced_credential_indicator is None
    assert lic.permit_indicator is None
