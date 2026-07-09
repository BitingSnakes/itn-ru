# rus_itn — C++ library

C++ Inverse Text Normalization for Russian built on plain [OpenFST](https://www.openfst.org)
(no pynini needed at runtime). It consumes grammars exported from the Python package and
reproduces the same pipeline (tag → reorder → verbalize, shortest path at each step);
output is byte-for-byte identical to `rus.normalize`.

## 1. Export the grammars (one-time, needs Python + pynini)

```shell
uv run python -m rus.export grammars_export
```

This writes `rus_itn_tagger.fst`, `rus_itn_verbalizer.fst` (plain OpenFST binaries,
loadable with `fst::StdVectorFst::Read`) and `rus_itn.far` (both grammars in one FAR
archive, keys `TAGGER` / `VERBALIZER`).

## 2. Build

```shell
brew install openfst cmake   # macOS; on Debian/Ubuntu: apt install libfst-dev cmake
cmake -B build -S cpp
cmake --build build
```

Produces `librus_itn.a` and the `rus_itn_cli` demo binary.

## 3. Use

Command line:

```shell
echo "двадцать две тысячи сто один" | ./build/rus_itn_cli grammars_export
# 22101
```

As a library:

```cpp
#include "rus_itn/rus_itn.h"

std::string error;
auto itn = rus_itn::InverseNormalizer::FromFiles(
    "grammars_export/rus_itn_tagger.fst",
    "grammars_export/rus_itn_verbalizer.fst", &error);

std::string out;
if (itn->Normalize("седьмой час двадцать пять минут", &out)) {
  // out == "07:25"
}
// or, never fails:
std::string out2 = itn->NormalizeOrPassthrough("любой текст");
```

Link against `rus_itn` and OpenFST (`-lfst`). The normalizer is immutable after
construction; `Normalize` is safe to call concurrently from multiple threads.
