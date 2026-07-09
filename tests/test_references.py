import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("статья пятая часть вторая", "ст. 5 ч. 2"),
        ("страница сто двадцать", "с. 120"),
        ("параграф третий", "§ 3"),
        ("пункт два", "п. 2"),
        ("раздел седьмой", "разд. 7"),
    ],
)
def test_legal(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("счет два один", "счет 2:1"),
        ("з счетом три ноль", "з счетом 3:0"),
    ],
)
def test_score(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("версия два точка пять", "версия 2.5"),
        ("версии три точка десять точка один", "версии 3.10.1"),
        ("версия пять", "версия 5"),
    ],
)
def test_version(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("сто девяносто два точка сто шестьдесят восемь точка один точка один", "192.168.1.1"),
        ("десять точка ноль точка ноль точка один", "10.0.0.1"),
    ],
)
def test_ip(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("девяностые годы", "90-е годы"),
        ("в восьмидесятых годах", "в 80-х годах"),
        ("сороковые годы", "40-е годы"),
    ],
)
def test_decade(spoken, expected):
    assert normalize(spoken) == expected
