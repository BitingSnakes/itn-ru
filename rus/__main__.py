import argparse
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="rus-itn",
        description="Inverse Text Normalization (ITN) for Russian",
        usage='echo "это случилось девятнадцатого числа" | python -m rus',
    )
    parser.add_argument("-j", "--json", action="store_true", help="return result as JSON")
    parser.add_argument("-v", "--verbose", action="store_true", help="print original input alongside the normalized output")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__import__('rus').__version__}")
    args = parser.parse_args(argv)

    from rus.wfst import normalize

    status = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            print(normalize(line, args.json))
        except Exception as exc:  # a sentence the grammar cannot parse
            print(f"error: could not normalize {line!r}: {exc}", file=sys.stderr)
            status = 1
            continue
        if args.verbose:
            print(line)
    return status


if __name__ == "__main__":
    sys.exit(main())
