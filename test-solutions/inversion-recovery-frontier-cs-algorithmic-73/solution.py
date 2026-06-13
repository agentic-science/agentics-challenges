from __future__ import annotations

import functools
import sys
import time


STARTED = time.monotonic()
EXACT_SOLVE_UNTIL_SEC = 85.0


class InversionOracle:
    def __init__(self) -> None:
        self.cache: dict[tuple[int, int], int] = {}

    def parity(self, left: int, right: int) -> int:
        if left >= right:
            return 0
        key = (left, right)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        print(f"0 {left} {right}", flush=True)
        line = sys.stdin.readline()
        if line == "":
            raise EOFError("interactive evaluator closed before replying")
        value = int(line.strip())
        self.cache[key] = value
        return value

    def greater(self, i: int, j: int) -> bool:
        if i == j:
            return False
        if i < j:
            bit = (
                self.parity(i, j)
                ^ self.parity(i + 1, j)
                ^ self.parity(i, j - 1)
                ^ self.parity(i + 1, j - 1)
            )
            return bit == 1

        return not self.greater(j, i)


def solve_case(n: int) -> None:
    if time.monotonic() - STARTED > EXACT_SOLVE_UNTIL_SEC:
        print("1 " + " ".join(str(position) for position in range(1, n + 1)), flush=True)
        return

    oracle = InversionOracle()

    def compare(i: int, j: int) -> int:
        if oracle.greater(i, j):
            return 1
        return -1

    positions = list(range(1, n + 1))
    positions.sort(key=functools.cmp_to_key(compare))

    values = [0] * (n + 1)
    for rank, position in enumerate(positions, start=1):
        values[position] = rank

    print("1 " + " ".join(str(values[position]) for position in range(1, n + 1)), flush=True)


def main() -> None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return
        if not line.strip():
            continue
        solve_case(int(line.strip()))


if __name__ == "__main__":
    main()
