import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("от пяти до десяти процентов", "5–10 %"),
        ("от ста до двухсот километров", "100–200 км"),
        ("от двух до трех", "2–3"),
        ("две-три часа", "2–3 ч"),
        ("пять-шесть километров", "5–6 км"),
        ("сорок-пятьдесят минут", "40–50 мин"),
    ],
)
def test_range(spoken, expected):
    assert normalize(spoken) == expected


def test_range_does_not_shadow_time():
    assert normalize("седьмой час двадцать пять минут") == "07:25"


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("с девятого до восемнадцатого часа", "с 09:00 до 18:00"),
        ("от восьмого до семнадцатого часа", "от 08:00 до 17:00"),
    ],
)
def test_time_range(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("с первого по пятое января", "с 1 по 5 января"),
        ("от десятого до двадцатого марта", "от 10 до 20 марта"),
    ],
)
def test_date_range(spoken, expected):
    assert normalize(spoken) == expected


def test_time_range_requires_hour_word():
    # without «часа» the phrase may be about anything -> untouched
    assert normalize("с первой по пятую попытку") == "с первой по пятую попытку"


def test_invalid_time_range_hours_are_not_emitted():
    assert normalize("с двадцать пятого до двадцать шестого часа") != "с 25:00 до 26:00"


def test_invalid_date_range_days_are_not_emitted():
    assert normalize("с тридцать второго по тридцать третье января") != "с 32 по 33 января"
