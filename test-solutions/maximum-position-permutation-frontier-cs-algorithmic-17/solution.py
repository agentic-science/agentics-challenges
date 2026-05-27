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


def ask(left: int, right: int) -> int:
    print(f"? {left} {right}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    return int(line.strip())


def answer(pos: int) -> None:
    print(f"! {pos}", flush=True)


def solve_case(n: int) -> None:
    if n == 2:
        second = ask(1, 2)
        answer(2 if second == 1 else 1)
        return

    second = ask(1, n)
    if second == 1:
        left, right = 2, n
        while left < right:
            mid = (left + right) // 2
            if ask(second, mid) == second:
                right = mid
            else:
                left = mid + 1
        answer(left)
        return

    if second == n:
        left, right = 1, n - 1
        while left < right:
            mid = (left + right + 1) // 2
            if ask(mid, second) == second:
                left = mid
            else:
                right = mid - 1
        answer(left)
        return

    if ask(1, second) == second:
        left, right = 1, second - 1
        while left < right:
            mid = (left + right + 1) // 2
            if ask(mid, second) == second:
                left = mid
            else:
                right = mid - 1
        answer(left)
    else:
        left, right = second + 1, n
        while left < right:
            mid = (left + right) // 2
            if ask(second, mid) == second:
                right = mid
            else:
                left = mid + 1
        answer(left)


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
