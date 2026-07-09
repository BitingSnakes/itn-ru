import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("ноль один ноль тридцать", "01030"),
        ("ноль сорок девять ноль ноль", "04900"),
        ("ноль семь ноль ноль восемь", "07008"),
    ],
)
def test_code(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        # too short / too long for a postal code
        ("ноль шестьдесят семь", "ноль 67"),
        ("ноль шестьдесят семь сто двадцать три сорок пять шестьдесят семь", "06712345607"),
    ],
)
def test_code_no_false_positives(spoken, expected):
    assert normalize(spoken) == expected
