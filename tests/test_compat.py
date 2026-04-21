"""Deprecated PascalCase API lives in ``aamva_parser.compat``."""

from aamva_parser import Parse, parse
from aamva_parser.compat import Parse as ParseFromCompat


def test_parse_same_as_parse_from_compat() -> None:
    minimal = """
@
ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
DCSPUBLIC
DACJOHN"""
    assert Parse(minimal).first_name == parse(minimal).first_name
    assert ParseFromCompat(minimal).first_name == parse(minimal).first_name
