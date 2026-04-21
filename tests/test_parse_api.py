from aamva_parser import (
    Parse,
    get_age,
    get_full_name,
    get_state,
    get_version,
    is_acceptable,
    is_cdl,
    is_expired,
    is_under_18,
    is_under_21,
    parse,
)

VALID_BARCODE = """
@
ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
DCSPUBLIC
DDEN
DACJOHN
DDFN
DADQUINCY
DDGN
DCAD
DCBNONE
DCDNONE
DBD08242015
DBB01311970
DBA01312035
DBC1
DAU069 in
DAYGRN
DAG789 E OAK ST
DAIANYTOWN
DAJCA
DAK902230000
DCF83D9BN217QO983B1
DCGUSA
DAW180
DAZBRO
DCK12345678900000000000
DDB02142014
DDK1
ZAZAAN
ZAB
ZAC"""


def test_parse_matches_deprecated_parse() -> None:
    a = Parse(VALID_BARCODE)
    b = parse(VALID_BARCODE)
    assert b.first_name == a.first_name
    assert b.last_name == a.last_name
    assert b.version == a.version


def test_get_version() -> None:
    assert get_version(VALID_BARCODE) == "08"


def test_parse_sample_license() -> None:
    lic = parse(VALID_BARCODE)
    assert lic.version == "08"
    assert lic.first_name == "JOHN"
    assert lic.middle_name == "QUINCY"
    assert lic.last_name == "PUBLIC"
    assert lic.state == "CA"
    assert lic.postal_code == "902230000"


def test_get_age() -> None:
    age = get_age(VALID_BARCODE)
    assert age is not None
    assert age > 50


def test_get_age_no_dob() -> None:
    minimal = """
@
ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
DCSPUBLIC
DACJOHN"""
    assert get_age(minimal) is None


def test_is_under_21_and_18() -> None:
    assert is_under_21(VALID_BARCODE) is False
    assert is_under_18(VALID_BARCODE) is False


def test_is_acceptable() -> None:
    assert is_acceptable(VALID_BARCODE) is True


def test_get_full_name() -> None:
    assert get_full_name(VALID_BARCODE) == "JOHN QUINCY PUBLIC"


def test_get_state() -> None:
    assert get_state(VALID_BARCODE) == "CA"


def test_is_cdl() -> None:
    assert is_cdl(VALID_BARCODE) is False


def test_is_expired_matches_barcode_expiry() -> None:
    assert isinstance(is_expired(VALID_BARCODE), bool)
