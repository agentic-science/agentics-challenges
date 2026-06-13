from __future__ import annotations

import sys
from collections import deque


def read_int_line() -> list[int]:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return []
        if line.strip():
            return [int(token) for token in line.split()]


def ask(left: int, right: int) -> int:
    print(f"1 {left} {right}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed before answering a query")
    return int(line.strip())


def solve_case(n: int) -> list[int]:
    interval_edges: dict[tuple[int, int], int] = {}
    path_edges: list[tuple[int, int]] = []

    def internal_edges(left: int, right: int) -> int:
        if left >= right:
            return 0
        key = (left, right)
        value = interval_edges.get(key)
        if value is None:
            value = right - left + 1 - ask(left, right)
            interval_edges[key] = value
        return value

    def crossing_edges(a_left: int, a_right: int, b_left: int, b_right: int) -> int:
        if a_left > a_right or b_left > b_right:
            return 0
        return (
            internal_edges(a_left, b_right)
            - internal_edges(a_left, b_left - 1)
            - internal_edges(a_right + 1, b_right)
            + internal_edges(a_right + 1, b_left - 1)
        )

    def find_crossing(a_left: int, a_right: int, b_left: int, b_right: int, count: int) -> None:
        if count <= 0:
            return
        if a_left == a_right and b_left == b_right:
            path_edges.append((a_left, b_left))
            return
        if a_right - a_left >= b_right - b_left:
            mid = (a_left + a_right) // 2
            left_count = crossing_edges(a_left, mid, b_left, b_right)
            find_crossing(a_left, mid, b_left, b_right, left_count)
            find_crossing(mid + 1, a_right, b_left, b_right, count - left_count)
        else:
            mid = (b_left + b_right) // 2
            left_count = crossing_edges(a_left, a_right, b_left, mid)
            find_crossing(a_left, a_right, b_left, mid, left_count)
            find_crossing(a_left, a_right, mid + 1, b_right, count - left_count)

    def reconstruct(left: int, right: int, count: int) -> None:
        if left >= right or count <= 0:
            return
        mid = (left + right) // 2
        left_count = internal_edges(left, mid)
        right_count = internal_edges(mid + 1, right)
        reconstruct(left, mid, left_count)
        reconstruct(mid + 1, right, right_count)
        find_crossing(left, mid, mid + 1, right, count - left_count - right_count)

    reconstruct(1, n, internal_edges(1, n))

    adjacency: list[list[int]] = [[] for _ in range(n + 1)]
    for u, v in path_edges:
        adjacency[u].append(v)
        adjacency[v].append(u)

    start = 1
    for vertex in range(1, n + 1):
        if len(adjacency[vertex]) <= 1:
            start = vertex
            break

    labels = [0] * (n + 1)
    queue: deque[tuple[int, int]] = deque([(start, 0)])
    order: list[int] = []
    while queue:
        vertex, parent = queue.popleft()
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            if neighbor != parent:
                queue.append((neighbor, vertex))

    for value, position in enumerate(order, start=1):
        labels[position] = value
    return labels[1:]


def main() -> int:
    while True:
        header = read_int_line()
        if not header:
            return 0
        n, _limit_asks, _limit_swaps = header
        if n <= 0:
            return 0
        guess = solve_case(n)
        print("3 " + " ".join(str(value) for value in guess), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
