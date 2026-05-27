from __future__ import annotations

import itertools
import sys


def ask(left: int, right: int) -> int:
    print(f"1 {left} {right}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed before answering a query")
    return int(line.strip())


def count_segments(perm: tuple[int, ...], left: int, right: int) -> int:
    values = set(perm[left - 1 : right])
    segments = 0
    in_segment = False
    for value in range(min(values), max(values) + 1):
        if value in values:
            if not in_segment:
                segments += 1
                in_segment = True
        else:
            in_segment = False
    return segments


def solve_case(n: int, limit_asks: int) -> list[int]:
    if n > 8:
        return list(range(1, n + 1))

    observations: dict[tuple[int, int], int] = {}
    used = 0
    for left in range(1, n + 1):
        for right in range(left, n + 1):
            if used >= limit_asks:
                break
            observations[(left, right)] = ask(left, right)
            used += 1

    for perm in itertools.permutations(range(1, n + 1)):
        if all(count_segments(perm, left, right) == value for (left, right), value in observations.items()):
            return list(perm)
    return list(range(1, n + 1))


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        n, l1, _l2 = map(int, stripped.split())
        if n <= 0:
            return 0
        guess = solve_case(n, l1)
        print("3 " + " ".join(str(value) for value in guess), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
