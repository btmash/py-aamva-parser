from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from aamva_parser.enums import (
    EyeColor,
    Gender,
    HairColor,
    IssuingCountry,
    NameSuffix,
    Truncation,
)


@dataclass(slots=True)
class License:
    """Decoded AAMVA PDF417 record (one card scan)."""

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    expiration_date: datetime | None = None
    issue_date: datetime | None = None
    date_of_birth: datetime | None = None
    gender: Gender = Gender.UNKNOWN
    eye_color: EyeColor = EyeColor.UNKNOWN
    height: float | None = None
    street_address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    drivers_license_id: str | None = None
    document_id: str | None = None
    country: IssuingCountry = IssuingCountry.UNKNOWN
    middle_name_truncation: Truncation = Truncation.NONE
    first_name_truncation: Truncation = Truncation.NONE
    last_name_truncation: Truncation = Truncation.NONE
    street_address_supplement: str | None = None
    hair_color: HairColor = HairColor.UNKNOWN
    place_of_birth: str | None = None
    audit_information: str | None = None
    inventory_control_number: str | None = None
    last_name_alias: str | None = None
    first_name_alias: str | None = None
    suffix_alias: str | None = None
    suffix: NameSuffix = NameSuffix.UNKNOWN
    cdl_indicator: str | None = None
    non_domiciled_indicator: str | None = None
    enhanced_credential_indicator: str | None = None
    permit_indicator: str | None = None
    version: str | None = None
    pdf417: str | None = None
    expired: bool = False
    weight: str | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> License:
        known = {f.name for f in cls.__dataclass_fields__.values()}
        extra = set(data) - known
        if extra:
            raise TypeError(f"Unknown fields for {cls.__name__}: {sorted(extra)!s}")
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**cast(dict[str, Any], filtered))

    def is_expired(self) -> bool:
        return self.expiration_date is not None and datetime.now() > self.expiration_date

    def has_been_issued(self) -> bool:
        return self.issue_date is not None and datetime.now() > self.issue_date

    def is_acceptable(self) -> bool:
        return (
            not self.is_expired()
            and self.has_been_issued()
            and self.expiration_date is not None
            and self.last_name is not None
            and self.first_name is not None
            and self.middle_name is not None
            and self.issue_date is not None
            and self.date_of_birth is not None
            and self.height is not None
            and self.street_address is not None
            and self.city is not None
            and self.state is not None
            and self.postal_code is not None
            and self.document_id is not None
        )
