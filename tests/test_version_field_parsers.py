"""Parity with js-aamva-parser version*FieldParser.test.ts files."""

from __future__ import annotations

from aamva_parser.enums import Gender, IssuingCountry
from aamva_parser.version_field_parsers import (
    VersionEightFieldParser,
    VersionElevenFieldParser,
    VersionFiveFieldParser,
    VersionFourFieldParser,
    VersionNineFieldParser,
    VersionOneFieldParser,
    VersionSevenFieldParser,
    VersionSixFieldParser,
    VersionThreeFieldParser,
    VersionTwelveFieldParser,
    VersionTwoFieldParser,
)

DATA_V1 = """@

  ANSI 636026020102DL00410288ZA03290015DLDAQD12345678
  DABPUBLIC
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

DATA_V2 = """@

  ANSI 636026020102DL00410288ZA03290015DLDAQD12345678
  DCSPUBLIC
  DDEN
  DCTJOHN
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

DATA_V3 = """@
  ANSI 636031030001DL00300210DLDAQL532143890998309
  DCADM
  DCSLEWIS
  DCTSAMUEL
  DCUnone
  DAG1121 W YUKON CT
  DAH
  DAIWAUKESHA
  DAJWI
  DAK53219000000
  DCG
  DBC1
  DAU071 IN
  DCE8
  DAYGRN
  DBA10232013
  DBB02131986
  DBD07222008
  DCBnone
  DCDnone
  DCHNONE
  DCFOTJAR22082722193452112213"""

DATA_V4 = """@

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

DATA_V5 = DATA_V4

DATA_V6 = """
@
ANSI 636015060002DL00410280ZT01211007DLDCAC
DCBNONE
DCDNONE
DBA10232031
DCSSMITH
DDEN
DACANDREW
DDFN
DADTHOMAS
DDGN
DBD11062023
DBB10231946
DBC1
DAYHAZ
DAU087 in
DAG8130 SKY RIDGE POND ST
DAIANYTOWN
DAJTX
DAK761770000
DAQ42145201
DCF00121300011116256231
DCGUSA
DAZBRO
DCK10022062633
DCLWO
DDAF
DDB07112021
DAW350
ZTZTAN"""

DATA_V7 = DATA_V4

DATA_V8 = """@

  ANSI 636026080102DL00410288ZA03290015DLDAQD12345678
  DCSPUBLIC
  DDEN
  DACJACKSON
  DDFN
  DADJONES
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

DATA_V9 = """
@
ANSI 636015090002DL00410280ZT01211007DLDCAC
DCBNONE
DCDNONE
DBA10232031
DCSSMITH
DDEN
DACANDREW
DDFN
DADTHOMAS
DDGN
DBD11062023
DBB10231946
DBC1
DAYHAZ
DAU087 in
DAG8130 SKY RIDGE POND ST
DAIANYTOWN
DAJTX
DAK761770000
DAQ42145201
DCF00121300011116256231
DCGUSA
DAZBRO
DCK10022062633
DCLWO
DDAF
DDB07112021
DAW350
ZTZTAN"""

DATA_V11 = """
@
ANSI 636015110002DL00410280ZT01211007DLDCAC
DCBNONE
DCDNONE
DBA10232031
DCSSMITH
DDEN
DACJANE
DDFN
DADMARIE
DDGN
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
DCK10022062633
DDAF
DDB07112021
DAW140"""

DATA_V12 = """
@
ANSI 636015120002DL00410280ZT01211007DLDCAC
DCBNONE
DCDNONE
DBA10232031
DCSJOHNSON
DDEN
DACROBERT
DDFN
DADJAMES
DDGN
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
DCK20250301122334
DDAF
DDB01202024
DAW200
DDM1
DDN1
DDO1
DDP1"""

DATA_V12_MINIMAL = """
@
ANSI 636015120002DL00410280ZT01211007DLDCAC
DCBNONE
DBA10232031
DCSDOE
DACJANE
DBD03152025
DBB01011995
DBC2
DAU065 in
DAG123 MAIN ST
DAIDALLAS
DAJTX
DAK75201
DAQ11122233
DCF00112233445566778899
DCGUSA
DAW130"""


def test_version_one_first_and_last_name() -> None:
    parser = VersionOneFieldParser(DATA_V1)
    assert parser.parse_first_name() == "JOHN"
    assert parser.parse_last_name() == "PUBLIC"


def test_version_two_first_name() -> None:
    parser = VersionTwoFieldParser(DATA_V2)
    assert parser.parse_first_name() == "JOHN"


def test_version_three_first_last_city() -> None:
    parser = VersionThreeFieldParser(DATA_V3)
    assert parser.parse_first_name() == "SAMUEL"
    assert parser.parse_last_name() == "LEWIS"
    assert parser.parse_string("city") == "WAUKESHA"


def test_version_four_first_name() -> None:
    parser = VersionFourFieldParser(DATA_V4)
    assert parser.parse_first_name() == "JOHN"


def test_version_five_weight() -> None:
    parser = VersionFiveFieldParser(DATA_V5)
    assert parser.parse_string("weight") == "180"


def test_version_six_first_name() -> None:
    parser = VersionSixFieldParser(DATA_V6)
    assert parser.parse_first_name() == "ANDREW"


def test_version_seven_first_name() -> None:
    parser = VersionSevenFieldParser(DATA_V7)
    assert parser.parse_first_name() == "JOHN"


def test_version_eight_first_name_and_city() -> None:
    parser = VersionEightFieldParser(DATA_V8)
    assert parser.parse_first_name() == "JACKSON"
    assert parser.parse_string("city") == "ANYTOWN"


def test_version_nine_first_and_last_name() -> None:
    parser = VersionNineFieldParser(DATA_V9)
    assert parser.parse_first_name() == "ANDREW"
    assert parser.parse_last_name() == "SMITH"


def test_version_eleven_parsing() -> None:
    parser = VersionElevenFieldParser(DATA_V11)
    assert parser.parse_first_name() == "JANE"
    assert parser.parse_last_name() == "SMITH"
    assert parser.parse_middle_name() == "MARIE"
    dob = parser.parse_date_of_birth()
    assert dob is not None
    assert dob.year == 1990
    assert parser.parse_gender() == Gender.FEMALE
    assert parser.parse_string("city") == "ANYTOWN"
    assert parser.parse_string("state") == "TX"


def test_version_twelve_parsing() -> None:
    parser = VersionTwelveFieldParser(DATA_V12)
    assert parser.parse_first_name() == "ROBERT"
    assert parser.parse_last_name() == "JOHNSON"
    assert parser.parse_string("cdl_indicator") == "1"
    assert parser.parse_string("non_domiciled_indicator") == "1"
    assert parser.parse_string("enhanced_credential_indicator") == "1"
    assert parser.parse_string("permit_indicator") == "1"
    assert parser.parse_string("postal_code") == "77001"
    assert parser.parse_string("last_name_alias") is None
    assert parser.parse_string("first_name_alias") is None
    assert parser.parse_string("suffix_alias") is None
    assert parser.parse_country() == IssuingCountry.UNITED_STATES


def test_version_twelve_minimal_optional_cds_fields() -> None:
    min_parser = VersionTwelveFieldParser(DATA_V12_MINIMAL)
    assert min_parser.parse_string("cdl_indicator") is None
    assert min_parser.parse_string("non_domiciled_indicator") is None
    assert min_parser.parse_string("enhanced_credential_indicator") is None
    assert min_parser.parse_string("permit_indicator") is None
    assert min_parser.parse_first_name() == "JANE"
    assert min_parser.parse_last_name() == "DOE"
