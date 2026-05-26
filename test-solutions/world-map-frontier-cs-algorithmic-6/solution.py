from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
import sys


INF = 10**9


def shortest_paths(n: int, edges: set[tuple[int, int]]) -> tuple[list[list[int]], list[list[int]]]:
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    nxt = [[0] * (n + 1) for _ in range(n + 1)]
    for vertex in range(1, n + 1):
        dist[vertex][vertex] = 0
        nxt[vertex][vertex] = vertex
    for left, right in edges:
        dist[left][right] = dist[right][left] = 1
        nxt[left][right] = right
        nxt[right][left] = left
    for mid in range(1, n + 1):
        for left in range(1, n + 1):
            if dist[left][mid] >= INF:
                continue
            for right in range(1, n + 1):
                candidate = dist[left][mid] + dist[mid][right]
                if candidate < dist[left][right]:
                    dist[left][right] = candidate
                    nxt[left][right] = nxt[left][mid]
    return dist, nxt


def restore_path(start: int, end: int, nxt: list[list[int]]) -> list[int]:
    path = [start]
    while start != end:
        start = nxt[start][end]
        if start == 0:
            raise ValueError("graph is disconnected")
        path.append(start)
    return path


def min_pairing(odd: tuple[int, ...], dist: list[list[int]]) -> tuple[int, list[tuple[int, int]]]:
    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[int, tuple[tuple[int, int], ...]]:
        if mask == 0:
            return 0, ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        best_cost = INF
        best_pairs: tuple[tuple[int, int], ...] = ()
        remaining = mask ^ first_bit
        scan = remaining
        while scan:
            bit = scan & -scan
            second = bit.bit_length() - 1
            cost, pairs = solve(remaining ^ bit)
            cost += dist[odd[first]][odd[second]]
            if cost < best_cost:
                best_cost = cost
                best_pairs = ((odd[first], odd[second]),) + pairs
            scan ^= bit
        return best_cost, best_pairs

    cost, pairs = solve((1 << len(odd)) - 1)
    return cost, list(pairs)


def duplicated_paths_for_open_trail(
    n: int,
    edges: set[tuple[int, int]],
    dist: list[list[int]],
    nxt: list[list[int]],
) -> list[list[int]]:
    degrees = [0] * (n + 1)
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    odd = tuple(vertex for vertex in range(1, n + 1) if degrees[vertex] % 2 == 1)
    if not odd:
        return []

    best_pairs: list[tuple[int, int]] | None = None
    best_cost = INF
    for keep_left in odd:
        for keep_right in odd:
            if keep_left >= keep_right:
                continue
            paired = tuple(vertex for vertex in odd if vertex not in {keep_left, keep_right})
            cost, pairs = min_pairing(paired, dist)
            if cost < best_cost:
                best_cost = cost
                best_pairs = pairs

    if best_pairs is None:
        best_pairs = []
    return [restore_path(left, right, nxt) for left, right in best_pairs]


def euler_walk(n: int, edges: set[tuple[int, int]], extra_paths: list[list[int]]) -> list[int]:
    adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
    edge_id = 0

    def add_edge(left: int, right: int) -> None:
        nonlocal edge_id
        adjacency[left].append((right, edge_id))
        adjacency[right].append((left, edge_id))
        edge_id += 1

    for left, right in sorted(edges):
        add_edge(left, right)
    for path in extra_paths:
        for left, right in zip(path, path[1:]):
            add_edge(left, right)

    start = next((vertex for vertex in range(1, n + 1) if len(adjacency[vertex]) % 2 == 1), 1)
    used = [False] * edge_id
    stack = [start]
    walk: list[int] = []
    while stack:
        vertex = stack[-1]
        while adjacency[vertex] and used[adjacency[vertex][-1][1]]:
            adjacency[vertex].pop()
        if adjacency[vertex]:
            nxt_vertex, eid = adjacency[vertex].pop()
            used[eid] = True
            stack.append(nxt_vertex)
        else:
            walk.append(stack.pop())
    walk.reverse()
    return walk


def construct_sequence(n: int, edges: set[tuple[int, int]]) -> list[int]:
    if n == 1:
        return [1]
    dist, nxt = shortest_paths(n, edges)
    extra_paths = duplicated_paths_for_open_trail(n, edges, dist, nxt)
    sequence = euler_walk(n, edges, extra_paths)
    if len(sequence) > 240:
        raise ValueError("baseline construction exceeded K=240")
    return sequence


def main() -> int:
    tokens = [int(token) for token in sys.stdin.read().split()]
    if len(tokens) < 2:
        return 1
    n, m = tokens[0], tokens[1]
    edges = {tuple(sorted((tokens[index], tokens[index + 1]))) for index in range(2, 2 + 2 * m, 2)}
    sequence = construct_sequence(n, edges)
    k = len(sequence)
    print(k)
    print(" ".join([str(k)] * k))
    row = " ".join(str(value) for value in sequence)
    for _ in range(k):
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
