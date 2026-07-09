import pytest

from rus.utils import attach_punctuation, separate_punctuation
from rus.wfst import normalize


def test_separate_punctuation():
    assert separate_punctuation("сто рублей, спасибо!") == "сто рублей , спасибо !"


def test_attach_punctuation():
    assert attach_punctuation("₽100 , спасибо !") == "₽100, спасибо!"


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("сто рублей, пожалуйста!", "₽100, пожалуйста!"),
        ("это случилось две тысячи девятнадцатого числа.", "это случилось 2019-го числа."),
        ("сколько? двадцать два метра!", "сколько? 22 м!"),
        ("«седьмой час двадцать пять минут» — да.", "«07:25» — да."),
        ("цена (сто евро) подходит", "цена (€100) подходит"),
        ("две третьих, или шестьдесят семь процентов", "2/3, или 67 %"),
        # apostrophes and hyphens are word-internal and must survive
        ("что учно пятое", "что учно пятое"),
    ],
)
def test_normalize_with_punctuation(spoken, expected):
    assert normalize(spoken) == expected
