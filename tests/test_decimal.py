import pytest

from rus.taggers.cardinal import CardinalFst
from rus.taggers.decimal import DecimalFst
from rus.wfst import apply_fst_text, normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("ноль целых одна десятая", "0.1"),
        ("минус пять целых одна десятая", "-5.1"),
        ("пять целых одна десятая", "5.1"),
        ("двадцать пять целых одна десятая", "25.1"),
        ("тридцать целых одна сотая", "30.01"),
        ("тридцать целых семьдесят пять сотых", "30.75"),
        ("сто восемь целых шесть тысячных", "108.006"),
        ("сто восемь целых тридцать тысячных", "108.030"),
        ("сто восемь целых тридцать шесть тысячных", "108.036"),
        ("сто восемь целых сто тридцать шесть тысячных", "108.136"),
        ("тридцать целых одна сотая", "30.01"),
    ],
)
def test_decimal(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("минус пять целых и одна десятая", "-5.1"),
        ("пять целых и одна десятая", "5.1"),
        ("двадцать пять целых и одна десятая", "25.1"),
    ],
)
def test_decimal__delimiter_with_and(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("два и семь десятых", "2.7"),
        ("два и семь сотых", "2.07"),
        ("два и семь тысячных", "2.007"),
    ],
)
def test_decimal__optional_delimiter_with_and(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("семь десятых", "0.7"),
        ("семь сотых", "0.07"),
        ("семь тысячных", "0.007"),
        ("двадцать пять тысячных", "0.025"),
        ("точность прибора равна две сотых", "точность прибора равна 0.02"),
    ],
)
def test_decimal__only_fractional(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("минус пять целых и одна десятая миллиона", "-5.1 миллиона"),
        ("пять целых и одна десятая миллиардов", "5.1 миллиардов"),
        ("двадцать пять тысяч", "25000"),
    ],
)
def test_decimal__delimiter_with_quantity(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("минус пять целых и одна десятая миллиона", 'decimal { negative: "true" integer_part: "5" fractional_part: "1"  quantity: "миллиона" }'),
        ("два и семь десятых", 'decimal { integer_part: "2" fractional_part: "7" }'),
        ("минус пять целых и две десятых", 'decimal { negative: "true" integer_part: "5" fractional_part: "2" }'),
    ],
)
def test_decimal__delimiter_with_quantity__only_tagger(spoken, expected):
    tCardinalFst = CardinalFst()
    tDecimalFst = DecimalFst(cardinal=tCardinalFst)

    assert apply_fst_text(spoken, tDecimalFst.fst) == expected
