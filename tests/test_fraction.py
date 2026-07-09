import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("одна вторая", "1/2"),
        ("одна третья", "1/3"),
        ("одна четверть", "1/4"),
        ("две третьих", "2/3"),
        ("две третьи", "2/3"),
        ("три четвертых", "3/4"),
        ("семь восьмых", "7/8"),
        ("пять шестых", "5/6"),
        ("одна двадцать пятая", "1/25"),
        ("минус три двадцать пятых", "-3/25"),
        ("три шестнадцатых", "3/16"),
        ("одна седьмая", "1/7"),
    ],
)
def test_fraction(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        # powers of ten must stay decimals
        ("одна десятая", "0.1"),
        ("ноль целых одна десятая", "0.1"),
        # time grammar must keep четверть phrases
        ("без четверти одиннадцатая", "10:45"),
        ("четверть одиннадцатого", "10:15"),
    ],
)
def test_fraction_does_not_shadow_other_classes(spoken, expected):
    assert normalize(spoken) == expected
