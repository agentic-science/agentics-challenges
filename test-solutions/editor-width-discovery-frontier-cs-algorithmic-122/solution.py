from __future__ import annotations

import sys


def read_int() -> int | None:
    line = sys.stdin.readline()
    if not line:
        return None
    try:
        return int(line.strip())
    except ValueError:
        return None


def solve_one() -> bool:
    # The first article [2, 1] makes the source interactor narrow W to {1, 2}.
    print("? 2 2 1", flush=True)
    first = read_int()
    if first is None or first == -1:
        return False

    # A single word of length 2 distinguishes the two remaining widths.
    print("? 1 2", flush=True)
    second = read_int()
    if second is None or second == -1:
        return False

    guess = 2 if second > 0 else 1
    print(f"! {guess}", flush=True)
    return True


def main() -> int:
    while True:
        t = read_int()
        if t is None:
            return 0
        for _ in range(t):
            if not solve_one():
                return 0


if __name__ == "__main__":
    raise SystemExit(main())
