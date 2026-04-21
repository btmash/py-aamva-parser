# py-aamva-parser

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: ISC](https://img.shields.io/badge/License-ISC-green.svg)](https://opensource.org/licenses/ISC)
[![Typed](https://img.shields.io/badge/Typed-py.typed-blue)](https://github.com/btmash/py-aamva-parser)

Python library to parse **AAMVA PDF417** barcode payloads from US and Canadian driver's licenses and ID cards.

This project is a **Python port** of **[aamva-parser](https://github.com/joptimus/aamva-parser)** by [joptimus](https://github.com/joptimus), originally implemented in **TypeScript** for Node.js. Parsing logic, version-specific field maps, and helpers are intended to track that upstream project.

The port was **produced with AI assistance** and **reviewed by a human** before publication.

If you use the JavaScript package, see its [README](https://github.com/joptimus/aamva-parser/blob/main/README.md) for the canonical API and field documentation.

**Repository:** [https://github.com/btmash/py-aamva-parser](https://github.com/btmash/py-aamva-parser)

**Copyright:** Ashok Modi (see [`LICENSE`](LICENSE)). **GitHub:** [@btmash](https://github.com/btmash).

Supports AAMVA barcode versions **01–12** (CDS 2000–2025). Includes helpers for age checks, full name formatting, and CDL detection (v12).

## Python vs JavaScript API

The Python package uses **idiomatic `snake_case`** on the `License` object and in module-level helpers (for example `date_of_birth`, `is_cdl`, `get_full_name`). The npm package uses **camelCase** (`dateOfBirth`, `isCDL`, `getFullName`).

Behavior is aligned with the TypeScript port where possible. Enums are Python `str` enums with the same string values as in JS (for example `Gender.MALE` → `"Male"`).

### `ParsedLicense` and `License` (for TypeScript users)

In the [upstream npm package](https://github.com/joptimus/aamva-parser), **`ParsedLicense`** is a TypeScript **interface**: it describes the shape of the object returned by `parse()` (fields plus methods like `isExpired()`). **`License`** is the **class** that implements that interface.

In Python there is **one** concrete type, the **`License`** dataclass, which is what `parse()` returns. **`ParsedLicense`** is exported as a [`typing.TypeAlias`](https://docs.python.org/3/library/typing.html#type-aliases) to `License`, so you can write the same style of annotations you would in TypeScript without learning a second runtime model:

```python
from aamva_parser import ParsedLicense, parse

def audit_card(payload: str, record: ParsedLicense) -> None:
    lic = parse(payload)
    assert lic.is_acceptable() == record.is_acceptable()
```

At runtime, `isinstance(lic, License)` and `isinstance(lic, ParsedLicense)` are equivalent.

## Requirements

- Python **3.10+**

## Installation

The **PyPI / pip name** is `aamva-parser` (hyphen). The **import name** is `aamva_parser` (underscore): `import aamva_parser` or `from aamva_parser import parse`.

**From PyPI** (when published):

```bash
pip install aamva-parser
```

**From a git checkout:**

```bash
pip install .
pip install -e ".[dev]"   # editable, with dev dependencies
```

The importable package name is **`aamva_parser`** (underscore).

### Poetry

This repo uses **[PEP 621](https://peps.python.org/pep-0621/)** metadata in `pyproject.toml` with **setuptools** as the build backend. Use **[Poetry 2.0+](https://python-poetry.org/)** so Poetry reads that layout without a legacy `[tool.poetry]` section.

**Add the library to another project** (PyPI, local path, or Git):

```bash
poetry add aamva-parser
poetry add ../py-aamva-parser
poetry add git+https://github.com/btmash/py-aamva-parser.git
```

**Develop this repo** (clone, install project + `dev` extra, run tests):

```bash
git clone https://github.com/btmash/py-aamva-parser.git
cd py-aamva-parser
poetry install -E dev
poetry run pytest
```

Use `poetry shell` to activate the environment, then run commands without `poetry run`. The `-E dev` flag installs the optional **`dev`** extra from `pyproject.toml` (currently `pytest`).

After dependency changes, run `poetry lock`. Commit `poetry.lock` if you want reproducible installs for Poetry users.

## Usage

### Parse a barcode

```python
from aamva_parser import ParsedLicense, parse, get_version, is_expired, get_age, is_under_21, get_full_name

barcode_data = """
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
ZAC
"""

lic = parse(barcode_data)

print(lic.first_name)       # "JOHN"
print(lic.last_name)        # "PUBLIC"
print(lic.date_of_birth)    # datetime.datetime(1970, 1, 31, 0, 0)
print(lic.expiration_date)  # datetime.datetime(2035, 1, 31, 0, 0)
print(lic.expired)          # False (snapshot from parsed expiry vs "now")

age = get_age(barcode_data)
under_21 = is_under_21(barcode_data)
name = get_full_name(barcode_data)  # "JOHN QUINCY PUBLIC"

expired = is_expired(barcode_data)
version = get_version(barcode_data)  # "08"
```

### Typing and enums

```python
from aamva_parser import parse, License, Gender, EyeColor

lic: License = parse(barcode_data)

if lic.gender == Gender.MALE:
    print("Male")

if lic.eye_color == EyeColor.GREEN:
    print("Green eyes")
```

### `LicenseParser` class

For multiple operations on the same raw string:

```python
from aamva_parser import LicenseParser

parser = LicenseParser(barcode_data)
version = parser.parse_version()
lic = parser.parse()
```

## API

The package exports **`License`** (concrete result type), **`ParsedLicense`** (same type, for annotations mirroring upstream TypeScript), enums, and **`LicenseParser`**. Module-level functions:

Each helper such as `get_full_name(barcode)` or `is_acceptable(barcode)` runs **`parse(barcode)`** internally. For hot paths, build one **`LicenseParser`** and call **`parse()`** once, then read fields or call **`License`** methods.

Deprecated **`Parse` / `GetVersion` / `IsExpired`** (PascalCase) live in **`aamva_parser.compat`** and are re-exported from the package root for npm parity; prefer snake_case.

| Function | Returns | Description |
| --- | --- | --- |
| `parse(barcode_data)` | `License` | Parse PDF417 payload into a `License`. |
| `get_version(barcode_data)` | `str \| None` | AAMVA version (e.g. `"08"`). |
| `is_expired(barcode_data)` | `bool` | Whether the expiration date is in the past. |
| `get_age(barcode_data)` | `int \| None` | Age in years, or `None` without DOB. |
| `is_under_21(barcode_data)` | `bool` | Under 21, or `False` if 21+ or no DOB. |
| `is_under_18(barcode_data)` | `bool` | Under 18, or `False` if 18+ or no DOB. |
| `is_acceptable(barcode_data)` | `bool` | Not expired, issued, and required fields set. |
| `get_full_name(barcode_data)` | `str \| None` | `"FIRST MIDDLE LAST"`; `None` if no names. |
| `get_state(barcode_data)` | `str \| None` | Jurisdiction (e.g. `"CA"`). |
| `is_cdl(barcode_data)` | `bool` | CDL indicator set (v12 / CDS 2025). |

### Deprecated aliases (JS compatibility)

| Deprecated | Use instead |
| --- | --- |
| `Parse()` | `parse()` |
| `GetVersion()` | `get_version()` |
| `IsExpired()` | `is_expired()` |

### `License` methods

- `is_expired()` — compare `expiration_date` to the current time.
- `has_been_issued()` — `True` if `issue_date` is in the past.
- `is_acceptable()` — stricter checklist (name, address, dates, document ID, etc.).

## Supported fields (`License`)

| Field | Type | Attribute |
| --- | --- | --- |
| First name | `str \| None` | `first_name` |
| Last name | `str \| None` | `last_name` |
| Middle name | `str \| None` | `middle_name` |
| Expiration date | `datetime \| None` | `expiration_date` |
| Issue date | `datetime \| None` | `issue_date` |
| Date of birth | `datetime \| None` | `date_of_birth` |
| Gender | `Gender` | `gender` |
| Eye color | `EyeColor` | `eye_color` |
| Hair color | `HairColor` | `hair_color` |
| Height (inches) | `float \| None` | `height` |
| Weight | `str \| None` | `weight` |
| Street address | `str \| None` | `street_address` |
| Street address line 2 | `str \| None` | `street_address_supplement` |
| City | `str \| None` | `city` |
| State | `str \| None` | `state` |
| Postal code | `str \| None` | `postal_code` |
| Driver's license ID | `str \| None` | `drivers_license_id` |
| Document ID | `str \| None` | `document_id` |
| Issuing country | `IssuingCountry` | `country` |
| Name suffix | `NameSuffix` | `suffix` |
| First name truncation | `Truncation` | `first_name_truncation` |
| Middle name truncation | `Truncation` | `middle_name_truncation` |
| Last name truncation | `Truncation` | `last_name_truncation` |
| Place of birth | `str \| None` | `place_of_birth` |
| Audit information | `str \| None` | `audit_information` |
| Inventory control number | `str \| None` | `inventory_control_number` |
| First name alias | `str \| None` | `first_name_alias` |
| Last name alias | `str \| None` | `last_name_alias` |
| Suffix alias | `str \| None` | `suffix_alias` |
| CDL indicator | `str \| None` | `cdl_indicator` |
| Non-domiciled indicator | `str \| None` | `non_domiciled_indicator` |
| Enhanced credential indicator | `str \| None` | `enhanced_credential_indicator` |
| Permit indicator | `str \| None` | `permit_indicator` |
| Expired (parsed snapshot) | `bool` | `expired` |
| AAMVA version | `str \| None` | `version` |
| Raw barcode | `str \| None` | `pdf417` |

## AAMVA version support

| CDS | Year | Barcode | Supported |
| --- | --- | --- | --- |
| 2000 | 2000 | 01 | Yes |
| 2003 | 2003 | 02 | Yes |
| 2005 | 2005 | 03 | Yes |
| 2009 | 2009 | 04–05 | Yes |
| 2010 | 2010 | 06 | Yes |
| 2011 | 2011 | 07 | Yes |
| 2012 | 2012 | 08 | Yes |
| 2013 | 2013 | 09 | Yes |
| 2016 | 2016 | 10 | Yes |
| 2020 | 2020 | 11 | Yes |
| 2025 | 2025 | 12 | Yes |

## Example

### Raw PDF417 payload (version 08)

```
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
ZAC
```

### Parsed values (illustrative)

```python
# After lic = parse(barcode_data)
{
    "first_name": "JOHN",
    "last_name": "PUBLIC",
    "middle_name": "QUINCY",
    "date_of_birth": datetime(1970, 1, 31),
    "expiration_date": datetime(2035, 1, 31),
    "issue_date": datetime(2015, 8, 24),
    "gender": Gender.MALE,
    "eye_color": EyeColor.GREEN,
    "hair_color": HairColor.BROWN,
    "height": 69,
    "weight": "180",
    "street_address": "789 E OAK ST",
    "city": "ANYTOWN",
    "state": "CA",
    "postal_code": "902230000",
    "drivers_license_id": "D12345678",
    "document_id": "83D9BN217QO983B1",
    "country": IssuingCountry.UNITED_STATES,
    "inventory_control_number": "12345678900000000000",
    "expired": False,
    "version": "08",
}
```

## AAMVA element IDs by version

**Bold** = mandatory in upstream docs. **`--`** = not used in that barcode version.

Tables are split so they fit typical viewports; the two halves are the same data as one wide 01–12 grid.

### Versions 01–06

| Field | 01 | 02 | 03 | 04 | 05 | 06 |
| --- | --- | --- | --- | --- | --- | --- |
| First Name | DAC | **DCT** | **DCT** | **DAC** | **DAC** | **DAC** |
| Last Name | DAB | **DCS** | **DCS** | **DCS** | **DCS** | **DCS** |
| Middle Name | DAD | **DAD** | **DAD** | **DAD** | **DAD** | **DAD** |
| Expiration Date | **DBA** | **DBA** | **DBA** | **DBA** | **DBA** | **DBA** |
| Issue Date | **DBD** | **DBD** | **DBD** | **DBD** | **DBD** | **DBD** |
| Date of Birth | **DBB** | **DBB** | **DBB** | **DBB** | **DBB** | **DBB** |
| Gender | **DBC** | **DBC** | **DBC** | **DBC** | **DBC** | **DBC** |
| Eye Color | DAY | **DAY** | **DAY** | **DAY** | **DAY** | **DAY** |
| Height | DAU | **DAU** | **DAU** | **DAU** | **DAU** | **DAU** |
| Street Address | **DAG** | **DAG** | **DAG** | **DAG** | **DAG** | **DAG** |
| City | **DAI** | **DAI** | **DAI** | **DAI** | **DAI** | **DAI** |
| State | **DAJ** | **DAJ** | **DAJ** | **DAJ** | **DAJ** | **DAJ** |
| Postal Code | **DAK** | **DAK** | **DAK** | **DAK** | **DAK** | **DAK** |
| License ID | **DBJ** | **DAQ** | **DAQ** | **DAQ** | **DAQ** | **DAQ** |
| Document ID | `--` | **DCF** | **DCF** | **DCF** | **DCF** | **DCF** |
| Country | `--` | **DCG** | **DCG** | **DCG** | **DCG** | **DCG** |
| Weight | `--` | DAW | DAW | DAW | DAW | DAW |
| CDL Indicator | `--` | `--` | `--` | `--` | `--` | `--` |
| Non-Domiciled Indicator | `--` | `--` | `--` | `--` | `--` | `--` |
| Enhanced Credential | `--` | `--` | `--` | `--` | `--` | `--` |
| Permit Indicator | `--` | `--` | `--` | `--` | `--` | `--` |

### Versions 07–12

| Field | 07 | 08 | 09 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- |
| First Name | **DAC** | **DAC** | **DAC** | **DAC** | **DAC** | **DAC** |
| Last Name | **DCS** | **DCS** | **DCS** | **DCS** | **DCS** | **DCS** |
| Middle Name | **DAD** | **DAD** | **DAD** | **DAD** | **DAD** | **DAD** |
| Expiration Date | **DBA** | **DBA** | **DBA** | **DBA** | **DBA** | **DBA** |
| Issue Date | **DBD** | **DBD** | **DBD** | **DBD** | **DBD** | **DBD** |
| Date of Birth | **DBB** | **DBB** | **DBB** | **DBB** | **DBB** | **DBB** |
| Gender | **DBC** | **DBC** | **DBC** | **DBC** | **DBC** | **DBC** |
| Eye Color | **DAY** | **DAY** | **DAY** | **DAY** | **DAY** | **DAY** |
| Height | **DAU** | **DAU** | **DAU** | **DAU** | **DAU** | **DAU** |
| Street Address | **DAG** | **DAG** | **DAG** | **DAG** | **DAG** | **DAG** |
| City | **DAI** | **DAI** | **DAI** | **DAI** | **DAI** | **DAI** |
| State | **DAJ** | **DAJ** | **DAJ** | **DAJ** | **DAJ** | **DAJ** |
| Postal Code | **DAK** | **DAK** | **DAK** | **DAK** | **DAK** | **DAK** |
| License ID | **DAQ** | **DAQ** | **DAQ** | **DAQ** | **DAQ** | **DAQ** |
| Document ID | **DCF** | **DCF** | **DCF** | **DCF** | **DCF** | **DCF** |
| Country | **DCG** | **DCG** | **DCG** | **DCG** | **DCG** | **DCG** |
| Weight | DAW | DAW | DAW | DAW | DAW | DAW |
| CDL Indicator | `--` | `--` | `--` | `--` | `--` | DDM |
| Non-Domiciled Indicator | `--` | `--` | `--` | `--` | `--` | DDN |
| Enhanced Credential | `--` | `--` | `--` | `--` | `--` | DDO |
| Permit Indicator | `--` | `--` | `--` | `--` | `--` | DDP |

## Development

Automated tests mirror the upstream Jest layout under `js-aamva-parser/tests/` (for example `regex.test.ts` → `tests/test_regex.py`, `indexApi.test.ts` → `tests/test_index_api.py`). Deprecated PascalCase helpers are implemented in `src/aamva_parser/compat.py`.

### pip and venv

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
ruff check src tests
ruff format --check src tests
mypy
pytest
```

### Poetry

From the repository root (Poetry 2.0+):

```bash
poetry install -E dev
poetry run ruff check src tests
poetry run ruff format --check src tests
poetry run mypy
poetry run pytest
```

Optional: `poetry shell`, then run the same commands without the `poetry run` prefix.

## License

This project is released under the **ISC License**. The copyright notice uses the author's legal name; see the [`LICENSE`](LICENSE) file. Source code and issues live under GitHub user [**btmash**](https://github.com/btmash).

## Credits

- **Python port:** maintained by [btmash](https://github.com/btmash) ([py-aamva-parser](https://github.com/btmash/py-aamva-parser)).
- **Upstream:** [aamva-parser](https://github.com/joptimus/aamva-parser) by [joptimus](https://github.com/joptimus) (TypeScript / Node.js).
- The original JavaScript README credits inspiration from the Swift project [ksoftllc/license-parser](https://github.com/ksoftllc/license-parser).
