import pytest

from rus.taggers.whitelist import WhitelistFst as Tagger
from rus.verbalizers.whitelist import WhitelistFst as Verbalizer
from rus.wfst import apply_fst_text, normalize


@pytest.mark.parametrize(
    "spoken,expected",
    [
        ("отправь эс эм эс", "отправь SMS"),
        ("подключи ю эс би и вай фай", "подключи USB и Wi-Fi"),
        ("джи пи эс и эй ай", "GPS и AI"),
        ("ЭС ЭМ ЭС", "SMS"),
    ],
)
def test_whitelist(spoken, expected):
    assert normalize(spoken) == expected


def test_whitelist_tagger_and_verbalizer():
    tagged = apply_fst_text("эс эм эс", Tagger().fst)
    assert tagged == 'whitelist { name: "SMS" }'
    assert apply_fst_text(tagged, Verbalizer().fst) == "SMS"


def test_whitelist_json():
    assert normalize("эс эм эс", json=True) == '[{"whitelist": "SMS"}]'

