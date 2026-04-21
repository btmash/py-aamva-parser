"""``ParsedLicense`` is a type alias to ``License`` (upstream TS pattern)."""

from aamva_parser import License, ParsedLicense, parse

VALID = """
@
ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
DCSPUBLIC
DACJOHN
DBB01311970
DBA01312035
DAJCA"""


def test_parse_returns_license_and_satisfies_parsed_license_alias() -> None:
    lic = parse(VALID)
    assert isinstance(lic, License)
    assert isinstance(lic, ParsedLicense)


def test_parsed_license_alias_is_license_class() -> None:
    assert ParsedLicense is License
