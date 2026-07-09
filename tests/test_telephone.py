import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        # grouped dictation (most common ASR pattern)
        ("восемь девятьсот двенадцать триста сорок пять шестьдесят семь восемьдесят девять", "89123456789"),
        # with ASR punctuation between groups
        ("восемь девятьсот двенадцать, триста сорок пять, шестьдесят семь, восемьдесят девять", "89123456789"),
        # international prefix, digit-by-digit
        ("плюс семь девятьсот двенадцать триста сорок пять шестьдесят семь восемьдесят девять", "+79123456789"),
        ("плюс семь девятьсот пятьдесят сто двадцать три сорок пять шестьдесят семь", "+79501234567"),
        # fully digit-by-digit
        ("восемь девять один два три четыре пять шесть семь восемь девять", "89123456789"),
        # mixed groups with bare tens (сорок -> 40)
        ("восемь девятьсот шестнадцать сорок сорок пять шестьдесят семь восемь", "89164045678"),
    ],
)
def test_telephone(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        # too short to be a phone number: stays as before
        ("ноль шестьдесят семь", "ноль 67"),
        ("двадцать две тысячи сто один", "22101"),
        ("ноль целых одна десятая", "0.1"),
    ],
)
def test_telephone_no_false_positives(spoken, expected):
    assert normalize(spoken) == expected
