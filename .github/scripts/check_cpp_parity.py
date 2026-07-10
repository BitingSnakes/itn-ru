"""Smoke-test byte-for-byte parity between the Python and C++ pipelines."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from rus import normalize

CASES = (
    "двадцать две тысячи сто один",
    "минус пять целых одна десятая процента",
    "одна вторая",
    "сто рублей, пожалуйста!",
    "первого января две тысячи первого года",
    "седьмой час двадцать пять минут",
    "восемь девятьсот двенадцать, триста сорок пять, шестьдесят семь, восемьдесят девять",
    "иван точка петренко собака джимейл точка ком",
    "девятнадцатый век",
    "от пяти до десяти процентов",
    "два часа тридцать минут",
    "в восьмидесятых годах",
    "статья пятая часть вторая",
    "счет три ноль",
    "версии три точка десять точка один",
    "сто девяносто два точка сто шестьдесят восемь точка один точка один",
    "ноль один ноль три ноль",
    "улица мира дом два корпус три квартира сорок",
    "Москва потратила СТО РУБЛЕЙ",
    "е\u0308лка потратила СТО РУБЛЕЙ",
    "минус пять рублей",
    "подключи ю эс би и вай фай",
    "третий час дня",
    "третий час пять минут по московскому времени",
    "двадцать\u00a0две тысячи сто один",
    "двадцать\u2003две тысячи сто один",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cli", type=Path)
    parser.add_argument("grammar_dir", type=Path)
    args = parser.parse_args()

    expected = [normalize(text) for text in CASES]
    completed = subprocess.run(
        [str(args.cli), str(args.grammar_dir)],
        input="".join(f"{text}\n" for text in CASES),
        text=True,
        capture_output=True,
        check=False,
    )
    actual = completed.stdout.splitlines()

    if completed.returncode != 0:
        print(completed.stderr, end="")
        return completed.returncode
    if len(actual) != len(expected):
        print(f"C++ returned {len(actual)} lines for {len(expected)} inputs")
        return 1

    mismatches = [
        (source, python_output, cpp_output)
        for source, python_output, cpp_output in zip(CASES, expected, actual)
        if python_output != cpp_output
    ]
    for source, python_output, cpp_output in mismatches:
        print(f"input:  {source}")
        print(f"python: {python_output}")
        print(f"c++:    {cpp_output}")
    if mismatches:
        return 1

    print(f"Python/C++ parity passed for {len(CASES)} representative inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
