from aamva_parser.regex_util import Regex


def test_first_match_returns_captured_group() -> None:
    regex = Regex()
    result = regex.first_match(r"hello (\w+)", "hello world")
    assert result == "world"


def test_first_match_returns_none_when_no_match() -> None:
    regex = Regex()
    result = regex.first_match(r"hello (\d+)", "hello world")
    assert result is None
