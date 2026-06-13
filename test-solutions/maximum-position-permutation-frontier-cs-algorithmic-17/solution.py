from __future__ import annotations

import sys

SEGMENT_SUM_MULT = 30


def read_int_line() -> int | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        line = line.strip()
        if line:
            return int(line)


class QueryBudget:
    def __init__(self, n: int) -> None:
        self.remaining_segment_sum = SEGMENT_SUM_MULT * n

    def consume(self, left: int, right: int) -> bool:
        length = right - left + 1
        if left >= right or length > self.remaining_segment_sum:
            return False
        self.remaining_segment_sum -= length
        return True


def ask(left: int, right: int, budget: QueryBudget) -> int | None:
    if not budget.consume(left, right):
        return None
    print(f"? {left} {right}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        return None
    return int(line.strip())


def answer(pos: int) -> None:
    print(f"! {pos}", flush=True)


def clamp_pos(pos: int, n: int) -> int:
    return min(max(pos, 1), n)


def solve_case(n: int) -> None:
    budget = QueryBudget(n)
    if n == 2:
        second = ask(1, 2, budget)
        answer(2 if second == 1 else 1)
        return

    second = ask(1, n, budget)
    if second is None:
        answer(1)
        return

    if second == 1:
        left, right = 2, n
        while left < right:
            mid = (left + right) // 2
            response = ask(second, mid, budget)
            if response is None:
                break
            if response == second:
                right = mid
            else:
                left = mid + 1
        answer(clamp_pos(left, n))
        return

    if second == n:
        left, right = 1, n - 1
        while left < right:
            mid = (left + right + 1) // 2
            response = ask(mid, second, budget)
            if response is None:
                break
            if response == second:
                left = mid
            else:
                right = mid - 1
        answer(clamp_pos(left, n))
        return

    side = ask(1, second, budget)
    if side is None:
        answer(clamp_pos(second, n))
        return

    if side == second:
        left, right = 1, second - 1
        while left < right:
            mid = (left + right + 1) // 2
            response = ask(mid, second, budget)
            if response is None:
                break
            if response == second:
                left = mid
            else:
                right = mid - 1
        answer(clamp_pos(left, n))
    else:
        left, right = second + 1, n
        while left < right:
            mid = (left + right) // 2
            response = ask(second, mid, budget)
            if response is None:
                break
            if response == second:
                right = mid
            else:
                left = mid + 1
        answer(clamp_pos(left, n))


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
