from __future__ import annotations

import sys


def ask_difference(delta: int) -> int:
    print(f"0 2 1 {1 + delta}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    return int(line.strip())


def solve_one_case(limit: int = 1000) -> None:
    for candidate in range(2, limit + 1):
        if ask_difference(candidate) > 0:
            print(f"1 {candidate}", flush=True)
            return
    print("1 2", flush=True)


def main() -> int:
    while True:
        try:
            solve_one_case()
        except (BrokenPipeError, EOFError):
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
