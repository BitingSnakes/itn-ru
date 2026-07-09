import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("две часа тридцать минут", "2 ч 30 мин"),
        ("три минуты двадцать секунд", "3 мин 20 с"),
        ("сорок минут", "40 мин"),
        ("двадцать четыре часа", "24 ч"),
        ("полтора часа", "1.5 ч"),
        ("полтора килограмма", "1.5 кг"),
        ("пол килограмма", "0.5 кг"),
        ("полчаса", "0.5 ч"),
    ],
)
def test_duration(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        # time-of-day idioms must stay with the TIME grammar
        ("седьмой час двадцать пять минут", "07:25"),
        ("пять минут двенадцатого", "11:05"),
        ("сорок семь минут двадцать второго", "21:47"),
        ("без четверти одиннадцатая", "10:45"),
    ],
)
def test_duration_does_not_shadow_time(spoken, expected):
    assert normalize(spoken) == expected
