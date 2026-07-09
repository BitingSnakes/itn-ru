# Changelog

### v0.2.0

- JSON output now safely escapes quotes, backslashes, control characters, and Unicode
  pass-through tokens.
- Added case-insensitive Russian classification with original spelling restoration for
  plain words, including NFC handling for precomposed and decomposed `ё`.
- Added negative money normalization (`"минус пять рублей"` -> `-₽5`).
- Fixed standalone thousandths (`"семь тысячных"` -> `0.007`) being misclassified as ordinals.
- Constrained numeric day, date-range day, clock hour/minute, time-range hour, and IPv4
  components to their supported domains.
- Hardened the C++ runtime with immutable thread-safe FSTs, strict UTF-8 validation,
  Python-equivalent Unicode whitespace handling, safe API failure semantics, native tests,
  and installable CMake package targets.
- Added Python/C++ CI, packaging checks, representative parity coverage, and C++ sources
  to the source distribution.
- Unified Python, lockfile, CMake, and distribution versions at 0.2.0.

### v0.1.0

- Init
