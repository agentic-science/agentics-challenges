from __future__ import annotations

import sys


def main() -> int:
    tokens = sys.stdin.read().split()
    if not tokens:
        return 1
    n = int(tokens[0])
    if n < 1:
        return 1
    print(1)
    print(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
