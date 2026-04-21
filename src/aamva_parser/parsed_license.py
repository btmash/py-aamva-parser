"""Typing alias mirroring the upstream ``ParsedLicense`` / ``License`` split.

In the TypeScript library, ``ParsedLicense`` is the **interface** describing the
shape and methods of a decoded barcode result. ``License`` is the **concrete
class** that implements that interface.

In Python there is a single concrete ``License`` dataclass; it already matches
that contract. ``ParsedLicense`` is a :class:`typing.TypeAlias` to ``License``
so you can annotate ``def handle(lic: ParsedLicense) -> None`` the same way
you would in TypeScript, without a second runtime type to learn.
"""

from __future__ import annotations

from typing import TypeAlias

from aamva_parser.license import License

ParsedLicense: TypeAlias = License

__all__ = ["ParsedLicense"]
