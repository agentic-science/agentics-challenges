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


def query(node: int) -> int:
    print(f"? {node}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    return int(line.strip())


def answer(node: int) -> None:
    print(f"! {node}", flush=True)


def solve_case(n: int) -> None:
    for _ in range(n - 1):
        sys.stdin.readline()
    if n >= 2 and query(2) == 1:
        answer(2)
    else:
        answer(1)


def main() -> int:
    while True:
        t = read_int_line()
        if t is None or t <= 0:
            return 0
        for _ in range(t):
            n = read_int_line()
            if n is None:
                return 0
            solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
