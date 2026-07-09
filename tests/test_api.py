import json
import subprocess
import sys

import pytest

import rus
from rus.wfst import InverseNormalizer, get_normalizer, normalize


def test_package_exports():
    assert rus.__version__ == "0.2.0"
    assert rus.normalize is normalize
    assert rus.InverseNormalizer is InverseNormalizer


def test_normalize_basic():
    assert normalize("двадцать две тысячи сто один") == "22101"


def test_normalize_is_case_insensitive_but_preserves_plain_words():
    assert normalize("Москва потратила СТО РУБЛЕЙ") == "Москва потратила ₽100"


def test_normalize_accepts_decomposed_yo_but_preserves_plain_words():
    assert normalize("пять рубле\u0308м") == "₽5"
    assert normalize("Е\u0308ж") == "Е\u0308ж"


def test_normalize_json():
    assert normalize("седьмой час двадцать пять минут", json=True) == '[{"time": "07:25"}]'


@pytest.mark.parametrize(
    "text",
    [
        'a"b',
        r"a\b",
        r"a\q",
        "эмодзи😀",
        "контроль\x01символ",
    ],
)
def test_normalize_json_preserves_arbitrary_words(text):
    assert json.loads(normalize(text, json=True)) == [{"word": text}]


def test_normalizer_is_singleton():
    assert get_normalizer() is get_normalizer()


def test_normalize_empty_raises():
    with pytest.raises(ValueError):
        normalize("   ")


def test_normalize_type_error():
    with pytest.raises(TypeError):
        normalize(None)


def test_cli_roundtrip():
    out = subprocess.run(
        [sys.executable, "-m", "rus"],
        input="двадцать две тысячи сто один\n",
        capture_output=True,
        text=True,
        check=True,
    )
    assert out.stdout.strip() == "22101"
