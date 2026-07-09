# WFST for Russian ITN

WFST-based Inverse Text Normalization (ITN) for Russian, built on NVIDIA NeMo grammars and Pynini.

Supported semiotic classes: cardinal, ordinal, decimal, fraction, measure, money, date, time,
telephone, electronic (e-mail/URL), century (Roman numerals), number sign (№), ranges
(numeric/time/date), durations & half-quantities, decades, legal references, scores,
versions, IPv4, postal codes, street addresses.
Punctuation-aware (built for ASR output): `"сто рублей, пожалуйста!"` -> `₽100, пожалуйста!`,
`"восемь девятьсот двенадцать, триста сорок пять, шестьдесят семь, восемьдесят девять"` -> `89123456789`
Uppercase input and precomposed/decomposed `ё` are accepted without changing the spelling
or case of ordinary pass-through words.

## Installation

```shell
brew install openfst   # needed to build pynini

export CPLUS_INCLUDE_PATH="/opt/homebrew/include:$CPLUS_INCLUDE_PATH"
export LIBRARY_PATH="/opt/homebrew/lib:$LIBRARY_PATH"

uv sync
```

## Usage

```python
from rus import normalize

normalize("это случилось две тысячи девятнадцатого числа")  # это случилось 2019-го числа
normalize("минус пять целых одна десятая процента")  # -5.1 %
normalize("двадцать две тысячи сто один")  # 22101
normalize("седьмой час двадцать пять минут")  # 07:25
normalize("МИНУС ПЯТЬ РУБЛЕЙ")  # -₽5
```

The grammars are built lazily on the first call (several seconds) and cached for the
lifetime of the process; subsequent calls take milliseconds. `normalize` is thread-safe.

### From command line

```shell
echo "это случилось две тысячи девятнадцатого числа" | python -m rus
# or, after `pip install rus_itn`:
echo "это случилось две тысячи девятнадцатого числа" | rus-itn
```

```
Options:
  -h, --help     Show this help message and exit
  -j, --json     Return result as JSON
  -v, --verbose  Print original input and normalized to compare
  --version      Show version
```

Will return `это случилось 2019-го числа`. Lines the grammar cannot parse are reported to
stderr and skipped (exit code 1).

### JSON output

For more advanced usage you can get json output

```python
from rus import normalize

normalize("это случилось две тысячи девятнадцатого числа", json=True)
# >>> '[{"word": "это"}, {"word": "случилось"}, {"ordinal": "2019"}, {"word": "числа"}]'
```

The returned string is valid JSON even when pass-through tokens contain quotes,
backslashes, control characters, or non-BMP Unicode.

## C++ library

The compiled grammars can be exported and used from C++ with plain OpenFST (no Python at
runtime):

```shell
uv run python -m rus.export grammars_export
cmake -B cpp/build -S cpp && cmake --build cpp/build
ctest --test-dir cpp/build --output-on-failure
echo "двадцать две тысячи сто один" | ./cpp/build/rus_itn_cli grammars_export  # 22101
```

See [cpp/README.md](cpp/README.md) for the library API.

## How it works

We have two kinds of FST: taggers and verbalizers.

This is a tagger:

```python
from rus.wfst import get_normalizer, apply_fst_text

apply_fst_text("минус пять целых одна десятая процента", get_normalizer().classify.fst)
```

will return `tokens { measure { negative: "true" integer_part: "5" fractional_part: "1" units: "%" } }`

And this is a verbalizer:

```python
from rus.wfst import get_normalizer, apply_fst_text

apply_fst_text('tokens { measure { negative: "true" integer_part: "5" fractional_part: "1" units: "%" } }',
               get_normalizer().verbalize_final.fst)
```

will return `-5.1 %`

## Development

```shell
uv sync                # install deps (dev group included)
uv run pytest          # run tests
uv run ruff check .    # lint
uv build               # build sdist + wheel
```
