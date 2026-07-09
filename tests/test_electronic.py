import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("иван точка петренко собака джимейл точка ком", "ivan.petrenko@gmail.com"),
        ("админ собака мейл ру", "admin@mail.ru"),
        ("олег девяносто девять собака гмейл точка ком", "oleg99@gmail.com"),
        ("инфо собака компания точка ком точка уа", "info@kompaniya.com.ua"),
        ("ве ве ве точка пример точка уа", "www.primer.ua"),
    ],
)
def test_electronic(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("собака лает", "собака лает"),
        ("точка с запятой", "точка с запятой"),
    ],
)
def test_electronic_no_false_positives(spoken, expected):
    assert normalize(spoken) == expected
