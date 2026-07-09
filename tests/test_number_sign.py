import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("номер пять", "№ 5"),
        ("под номером двадцать два", "под № 22"),
        ("номер сто один", "№ 101"),
    ],
)
def test_number_sign(spoken, expected):
    assert normalize(spoken) == expected
