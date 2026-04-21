from __future__ import annotations

from copy import copy
from typing import Protocol


class FieldMapping(Protocol):
    fields: dict[str, str]

    def field_for(self, key: str) -> str:
        ...


class FieldMapper:
    """Default AAMVA field designators (aligned with Version 8-style layout)."""

    def __init__(self) -> None:
        self._fields: dict[str, str] = {
            "first_name": "DAC",
            "last_name": "DCS",
            "middle_name": "DAD",
            "expiration_date": "DBA",
            "issue_date": "DBD",
            "date_of_birth": "DBB",
            "gender": "DBC",
            "eye_color": "DAY",
            "height": "DAU",
            "street_address": "DAG",
            "city": "DAI",
            "state": "DAJ",
            "postal_code": "DAK",
            "drivers_license_id": "DAQ",
            "document_id": "DCF",
            "country": "DCG",
            "middle_name_truncation": "DDG",
            "first_name_truncation": "DDF",
            "last_name_truncation": "DDE",
            "street_address_supplement": "DAH",
            "hair_color": "DAZ",
            "place_of_birth": "DCI",
            "audit_information": "DCJ",
            "inventory_control_number": "DCK",
            "last_name_alias": "DBN",
            "first_name_alias": "DBG",
            "suffix_alias": "DBS",
            "suffix": "DCU",
            "weight": "DAW",
        }

    @property
    def fields(self) -> dict[str, str]:
        return self._fields

    @fields.setter
    def fields(self, new_fields: dict[str, str]) -> None:
        self._fields = new_fields

    def field_for(self, key: str) -> str:
        return self._fields.get(key, "")

    def copy_fields(self) -> dict[str, str]:
        return copy(self._fields)
