from __future__ import annotations

import sys


def read_ints() -> list[int] | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        if line.strip():
            return [int(part) for part in line.split()]


def query(values: list[int]) -> list[int]:
    print(" ".join([str(len(values)), *[str(value) for value in values]]), flush=True)
    response = read_ints()
    if response is None:
        raise EOFError("interactor closed during query")
    return response


def pair_is_adjacent(a: int, b: int) -> bool:
    response = query([a, b])
    query([a, b])
    return bool(response and response[-1] == 1)


def recover_small_cycle(n: int) -> list[int]:
    neighbors: dict[int, list[int]] = {value: [] for value in range(1, n + 1)}
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            if pair_is_adjacent(a, b):
                neighbors[a].append(b)
                neighbors[b].append(a)

    if n == 1:
        return [1]
    if any(len(items) != 2 for items in neighbors.values()):
        return list(range(1, n + 1))

    order = [1]
    prev = 0
    cur = 1
    while len(order) < n:
        nxt = neighbors[cur][0] if neighbors[cur][0] != prev else neighbors[cur][1]
        if nxt in order:
            return list(range(1, n + 1))
        order.append(nxt)
        prev, cur = cur, nxt
    return order


def solve_case(subtask: int, n: int) -> None:
    del subtask
    if n <= 8:
        answer = recover_small_cycle(n)
    else:
        answer = list(range(1, n + 1))
    print(" ".join(["-1", *[str(value) for value in answer]]), flush=True)


def main() -> int:
    while True:
        header = read_ints()
        if header is None or len(header) < 2:
            return 0
        subtask, n = header[0], header[1]
        if subtask == 0 and n == 0:
            return 0
        solve_case(subtask, n)


if __name__ == "__main__":
    raise SystemExit(main())
