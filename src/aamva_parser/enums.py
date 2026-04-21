from __future__ import annotations

from enum import Enum


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class EyeColor(str, Enum):
    BLACK = "Black"
    BLUE = "Blue"
    BROWN = "Brown"
    GRAY = "Gray"
    GREEN = "Green"
    HAZEL = "Hazel"
    MAROON = "Maroon"
    PINK = "Pink"
    DICHROMATIC = "Dichromatic"
    UNKNOWN = "Unknown"


class HairColor(str, Enum):
    BALD = "Bald"
    BLACK = "Black"
    BLOND = "Blond"
    BROWN = "Brown"
    GREY = "Grey"
    RED = "Red"
    SANDY = "Sandy"
    WHITE = "White"
    UNKNOWN = "Unknown"


class IssuingCountry(str, Enum):
    UNITED_STATES = "United States"
    CANADA = "Canada"
    UNKNOWN = "Unknown"


class Truncation(str, Enum):
    TRUNCATED = "Truncated"
    NONE = "None"
    UNKNOWN = "Unknown"


class NameSuffix(str, Enum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    FIRST = "First"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"
    FIFTH = "Fifth"
    SIXTH = "Sixth"
    SEVENTH = "Seventh"
    EIGHTH = "Eighth"
    NINTH = "Ninth"
    UNKNOWN = "Unknown"
