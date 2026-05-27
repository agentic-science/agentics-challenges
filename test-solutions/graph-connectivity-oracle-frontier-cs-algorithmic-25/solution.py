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


def ask(bits: str) -> int:
    print(f"?# {bits}".replace(" ", ""), flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    return int(line.strip())


def answer(value: int) -> None:
    print(f"!#{value}", flush=True)


def solve_case(n: int) -> None:
    if n <= 11:
        for mask in range(1, (1 << n) - 1):
            bits = "".join("1" if mask & (1 << i) else "0" for i in range(n))
            if ask(bits) == 0:
                answer(0)
                return
        answer(1)
        return
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
