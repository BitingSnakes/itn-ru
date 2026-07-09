import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("девятнадцатый век", "XIX век"),
        ("в двадцать первом веке", "в XXI веке"),
        ("пятое столетие", "V столетие"),
        ("третьего тысячелетия", "III тысячелетия"),
    ],
)
def test_century(spoken, expected):
    assert normalize(spoken) == expected
