import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("первого января две тысячи первого года", "1 января 2001 года"),
        ("третье июня две тысячи двадцать третьего", "3 июня 2023"),
        ("первого января", "1 января"),
        ("двадцать первое февраля", "21 февраля"),
        ("январь две тысячи первого года", "январь 2001 года"),
        ("январь две тысячи первого", "январь 2001"),
        ("две тысячи первый год", "2001 год"),
        ("девятьсот сорок пятый год до нашей эры", "945 год до н. э."),
        ("сто восемьдесят восьмой год нашей эры", "188 год н. э."),
    ],
)
def test_month(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("пятого июля", "5 июля"),
        ("пятого июля две тысячи двадцатого года", "5 июля 2020 года"),
        ("июль две тысячи первого года", "июль 2001 года"),
    ],
)
def test_july(spoken, expected):
    assert normalize(spoken) == expected


def test_day_above_31_is_not_emitted_as_a_date():
    assert normalize("тридцать второе января") != "32 января"
