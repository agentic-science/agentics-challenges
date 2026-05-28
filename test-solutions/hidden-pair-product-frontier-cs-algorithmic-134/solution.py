from __future__ import annotations

import sys

REPEATS = 80


class FoundAnswer(Exception):
    pass


def ask(x: int, y: int) -> int:
    print(f"{x} {y}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    value = int(line.strip())
    if value == 0:
        raise FoundAnswer
    return value


def compare_a(x: int) -> int:
    """Return -1, 0, or 1 for x compared with the hidden first value."""
    for _ in range(REPEATS):
        response = ask(x, 1)
        if response == 1:
            return -1
        if response == 3:
            return 1
    return 0


def compare_b(y: int) -> int:
    """Return -1, 0, or 1 for y compared with the hidden second value."""
    for _ in range(REPEATS):
        response = ask(1, y)
        if response == 2:
            return -1
        if response == 3:
            return 1
    return 0


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        n = int(line.strip())

        try:
            lo, hi = 1, n
            while lo < hi:
                mid = (lo + hi) // 2
                if compare_a(mid) < 0:
                    lo = mid + 1
                else:
                    hi = mid
            a = lo

            lo, hi = 1, n
            while lo < hi:
                mid = (lo + hi) // 2
                if compare_b(mid) < 0:
                    lo = mid + 1
                else:
                    hi = mid
            print(f"{a} {lo}", flush=True)
            line = sys.stdin.readline()
            if not line:
                return 0
        except FoundAnswer:
            continue


if __name__ == "__main__":
    raise SystemExit(main())
