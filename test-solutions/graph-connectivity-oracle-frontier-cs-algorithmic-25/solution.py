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
    print(f"?#{bits}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    return int(line.strip())


def answer(value: int) -> None:
    print(f"!#{value}", flush=True)


def solve_case(n: int) -> None:
    if n <= 1:
        answer(1)
        return

    prefix = ["0"] * n
    for index in range(n - 1):
        prefix[index] = "1"
        if ask("".join(prefix)) == 0:
            answer(0)
            return

    answer(1)


def main() -> int:
    while True:
        test_count = read_int_line()
        if test_count is None or test_count <= 0:
            return 0
        for _ in range(test_count):
            n = read_int_line()
            if n is None:
                return 0
            solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
