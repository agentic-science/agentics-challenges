from __future__ import annotations

import sys

MAX_QUERIES_PER_CASE = 4096


def force(left: list[int], right: list[int]) -> int:
    print(f"? {len(left)} {len(right)}", flush=True)
    print(" ".join(map(str, left)), flush=True)
    print(" ".join(map(str, right)), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed during magnet query")
    return int(line.strip())


def solve_case(n: int) -> None:
    query_count = 0
    search_budget = max(0, MAX_QUERIES_PER_CASE - max(0, n - 1))

    def bounded_force(left: list[int], right: list[int]) -> int | None:
        nonlocal query_count
        if query_count >= MAX_QUERIES_PER_CASE:
            return None
        query_count += 1
        return force(left, right)

    anchor = 0

    def try_anchor_pair(i: int, j: int) -> bool:
        nonlocal anchor
        if i == j or query_count >= search_budget:
            return False
        result = bounded_force([i], [j])
        if result is None:
            return False
        if result != 0:
            anchor = i
            return True
        return False

    for j in range(2, n + 1):
        if try_anchor_pair(1, j):
            break
    offset = 1
    while not anchor and offset < n:
        for i in range(1, n + 1):
            j = ((i + offset - 1) % n) + 1
            if try_anchor_pair(i, j):
                break
        offset *= 2

    probe = 0
    while not anchor and query_count < search_budget:
        i = ((probe * 1103515245 + 12345) % n) + 1
        j = ((probe * 2654435761 + 1013904223) % n) + 1
        if i == j:
            j = (j % n) + 1
        try_anchor_pair(i, j)
        probe += 1

    if not anchor:
        print("! " + str(n) + " " + " ".join(map(str, range(1, n + 1))), flush=True)
        return

    demagnetized: list[int] = []
    for idx in range(1, n + 1):
        if idx == anchor:
            continue
        result = bounded_force([anchor], [idx])
        if result is None:
            break
        if result == 0:
            demagnetized.append(idx)

    suffix = " " + " ".join(map(str, demagnetized)) if demagnetized else ""
    print("! " + str(len(demagnetized)) + suffix, flush=True)


def main() -> int:
    first = sys.stdin.readline()
    if not first:
        return 0
    test_count = int(first.strip())
    if test_count <= 0:
        return 0
    for _ in range(test_count):
        line = sys.stdin.readline()
        if not line:
            return 0
        solve_case(int(line.strip()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
