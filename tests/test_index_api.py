"""Parity with js-aamva-parser tests/indexApi.test.ts."""

from aamva_parser import (
    GetVersion,
    IsExpired,
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


def test_get_version_matches_get_version_deprecated() -> None:
    assert get_version(VALID_BARCODE) == GetVersion(VALID_BARCODE)


def test_is_expired_matches_is_expired_deprecated() -> None:
    assert is_expired(VALID_BARCODE) == IsExpired(VALID_BARCODE)


def test_get_age() -> None:
    age = get_age(VALID_BARCODE)
    assert age is not None
    assert age > 50


def test_get_age_no_dob() -> None:
    no_dob = """
@
ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
DCSPUBLIC
DACJOHN"""
    assert get_age(no_dob) is None


def test_is_under_21() -> None:
    assert is_under_21(VALID_BARCODE) is False


def test_is_under_18() -> None:
    assert is_under_18(VALID_BARCODE) is False


def test_is_acceptable() -> None:
    assert is_acceptable(VALID_BARCODE) is True


def test_get_full_name() -> None:
    assert get_full_name(VALID_BARCODE) == "JOHN QUINCY PUBLIC"


def test_get_full_name_missing_middle() -> None:
    no_middle = """
@
ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
DCSPUBLIC
DACJOHN
DBD08242015
DBB01311970
DBA01312035
DBC1
DAU069 in
DAG789 E OAK ST
DAIANYTOWN
DAJCA
DAK902230000
DCF83D9BN217QO983B1
DCGUSA"""
    assert get_full_name(no_middle) == "JOHN PUBLIC"


def test_get_full_name_no_name_fields() -> None:
    empty = """
@
ANSI 636026080102DL00410288ZA03290015DL"""
    assert get_full_name(empty) is None


def test_get_state() -> None:
    assert get_state(VALID_BARCODE) == "CA"


def test_is_cdl_false_for_non_cdl() -> None:
    assert is_cdl(VALID_BARCODE) is False


def test_is_cdl_true_for_v12_cdl_barcode() -> None:
    cdl = """
@
ANSI 636015120002DL00410280ZT01211007DLDCAC
DCBNONE
DBA10232031
DCSJOHNSON
DACROBERT
DADJAMES
DBD03152025
DBB06151985
DBC1
DAYBLU
DAU072 in
DAG789 PINE ST
DAIHOUSTON
DAJTX
DAK77001
DAQ88834567
DCF00998877665544332211
DCGUSA
DAW200
DDM1"""
    assert is_cdl(cdl) is True
