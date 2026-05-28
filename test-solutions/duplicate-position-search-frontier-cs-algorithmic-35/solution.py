from __future__ import annotations

import itertools
import sys


BITS = 12
WEIGHT = 6


def read_int() -> int | None:
    line = sys.stdin.readline()
    if not line:
        return None
    try:
        return int(line.strip())
    except ValueError:
        return None


def ask(value: int, subset: list[int]) -> int:
    print(f"? {value} {len(subset)} " + " ".join(map(str, subset)), flush=True)
    reply = read_int()
    if reply is None or reply == -1:
        raise SystemExit(0)
    return reply


def solve_case(n: int, codes: list[tuple[int, ...]]) -> None:
    total_positions = 2 * n - 1
    subsets = [[] for _ in range(BITS)]
    for position, code in enumerate(codes[:total_positions], start=1):
        for bit in code:
            subsets[bit].append(position)

    answer = 1
    active_subsets = [subset for subset in subsets if subset]

    for value in range(1, n + 1):
        seen_bits = 0
        for subset in active_subsets:
            seen_bits += ask(value, subset)
        if seen_bits == WEIGHT:
            answer = value
            break

    print(f"! {answer}", flush=True)


def main() -> int:
    first = read_int()
    if first is None:
        return 0

    codes = list(itertools.combinations(range(BITS), WEIGHT))
    for _ in range(first):
        n = read_int()
        if n is None or n == -1:
            return 0
        solve_case(n, codes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
