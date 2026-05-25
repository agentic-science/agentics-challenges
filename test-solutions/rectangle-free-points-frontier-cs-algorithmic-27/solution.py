from __future__ import annotations

import sys


def main() -> int:
    tokens = sys.stdin.read().split()
    if len(tokens) < 2:
        return 1
    n, m = int(tokens[0]), int(tokens[1])

    if m <= n:
        print(n)
        for row in range(1, n + 1):
            print(row, 1)
    else:
        print(m)
        for col in range(1, m + 1):
            print(1, col)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
