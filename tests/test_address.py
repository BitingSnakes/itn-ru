import pytest

from rus.wfst import normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("улица шевченко дом пять квартира три", "ул. шевченко, д. 5, кв. 3"),
        ("улица ивана франка, дом семь, квартира девять", "ул. ивана франка, д. 7, кв. 9"),
        ("проспект победы дом сто двадцать", "просп. победы, д. 120"),
        ("улица мира дом два корпус три квартира сорок", "ул. мира, д. 2, корп. 3, кв. 40"),
    ],
)
def test_address(spoken, expected):
    assert normalize(spoken) == expected


def test_bare_street_untouched():
    # no house number -> no abbreviation
    assert normalize("на улице крещатик") == "на улице крещатик"
