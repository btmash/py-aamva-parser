"""Deprecated PascalCase entry points matching the upstream npm API.

Prefer :func:`aamva_parser.parse`, :func:`aamva_parser.get_version`, and
:func:`aamva_parser.is_expired` (snake_case, PEP 8).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aamva_parser.parsed_license import ParsedLicense


def Parse(barcode: str) -> ParsedLicense:
    from aamva_parser import parse as _parse

    return _parse(barcode)


def GetVersion(barcode: str) -> str | None:
    from aamva_parser import get_version as _get_version

    return _get_version(barcode)


def IsExpired(barcode: str) -> bool:
    from aamva_parser import is_expired as _is_expired

    return _is_expired(barcode)


__all__ = ["GetVersion", "IsExpired", "Parse"]
