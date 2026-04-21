from aamva_parser import get_version, parse

V11_DATA = """
@
ANSI 636015110002DL00410280ZT01211007DLDCAC
DCBNONE
DBA10232031
DCSSMITH
DACJANE
DADMARIE
DBD11062023
DBB10231990
DBC2
DAYBRO
DAU065 in
DAG456 OAK AVE
DAIANYTOWN
DAJTX
DAK761770000
DAQ55512345
DCF00121300011116256231
DCGUSA
DAZBLN
DAW140"""

V12_DATA = """
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
DAZBRN
DAW200
DDM1
DDO1"""


def test_version_11() -> None:
    assert get_version(V11_DATA) == "11"


def test_parse_v11() -> None:
    lic = parse(V11_DATA)
    assert lic.version == "11"
    assert lic.first_name == "JANE"
    assert lic.last_name == "SMITH"


def test_version_12() -> None:
    assert get_version(V12_DATA) == "12"


def test_parse_v12_cds_fields() -> None:
    lic = parse(V12_DATA)
    assert lic.version == "12"
    assert lic.first_name == "ROBERT"
    assert lic.last_name == "JOHNSON"
    assert lic.cdl_indicator == "1"
    assert lic.enhanced_credential_indicator == "1"
    assert lic.non_domiciled_indicator is None
    assert lic.permit_indicator is None
    assert lic.postal_code == "77001"
