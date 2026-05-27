from __future__ import annotations

import sys


def read_int_line() -> int | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        line = line.strip()
        if line:
            return int(line)


def ask(x: int, y: int) -> int:
    print(f"? {x} {y}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    return int(line.strip())


def answer(x: int, y: int) -> bool:
    print(f"! {x} {y}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        return False
    return int(line.strip()) == 1


def adjacent(n: int, x: int, y: int) -> bool:
    return abs(x - y) == 1 or abs(x - y) == n - 1


def solve_case(n: int) -> bool:
    if n <= 80:
        for x in range(1, n + 1):
            for y in range(x + 1, n + 1):
                if adjacent(n, x, y):
                    continue
                if ask(x, y) == 1:
                    return answer(x, y)
    return answer(1, 3)


def main() -> int:
    while True:
        t = read_int_line()
        if t is None or t <= 0:
            return 0
        for _ in range(t):
            n = read_int_line()
            if n is None:
                return 0
            if not solve_case(n):
                return 0


if __name__ == "__main__":
    raise SystemExit(main())
