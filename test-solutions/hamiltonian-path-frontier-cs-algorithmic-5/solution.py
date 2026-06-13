from __future__ import annotations

from collections import deque
import sys


def parse_input() -> tuple[int, list[int], list[set[int]], list[set[int]]]:
    values = [int(token) for token in sys.stdin.read().split()]
    if len(values) < 12:
        raise ValueError("input must contain n, m, and ten thresholds")
    n, m = values[0], values[1]
    if n < 1 or m < 0:
        raise ValueError("invalid graph size")
    edge_values = values[12:]
    if len(edge_values) < 2 * m:
        raise ValueError("not enough edge endpoints")

    outgoing = [set() for _ in range(n + 1)]
    incoming = [set() for _ in range(n + 1)]
    for index in range(0, 2 * m, 2):
        left, right = edge_values[index], edge_values[index + 1]
        if 1 <= left <= n and 1 <= right <= n and left != right:
            outgoing[left].add(right)
            incoming[right].add(left)
    return n, values[2:12], outgoing, incoming


def dag_longest_path(n: int, outgoing: list[set[int]], incoming: list[set[int]]) -> list[int] | None:
    indegree = [0] * (n + 1)
    for vertex in range(1, n + 1):
        indegree[vertex] = len(incoming[vertex])

    queue = deque(vertex for vertex in range(1, n + 1) if indegree[vertex] == 0)
    order: list[int] = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in sorted(outgoing[vertex]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != n:
        return None

    best = [1] * (n + 1)
    parent = [0] * (n + 1)
    for vertex in order:
        for neighbor in outgoing[vertex]:
            if best[vertex] + 1 > best[neighbor]:
                best[neighbor] = best[vertex] + 1
                parent[neighbor] = vertex

    end = max(range(1, n + 1), key=lambda vertex: (best[vertex], -vertex))
    path: list[int] = []
    while end:
        path.append(end)
        end = parent[end]
    path.reverse()
    return path


def choose_candidate(
    candidates: set[int],
    used: bytearray,
    outgoing: list[set[int]],
    incoming: list[set[int]],
    variant: int,
) -> int:
    best_vertex = 0
    best_key: tuple[int, int, int, int] | None = None
    for vertex in candidates:
        if used[vertex]:
            continue
        out_degree = len(outgoing[vertex])
        in_degree = len(incoming[vertex])
        if variant == 0:
            key = (out_degree, -in_degree, out_degree + in_degree, -vertex)
        elif variant == 1:
            key = (-in_degree, out_degree, out_degree + in_degree, -vertex)
        elif variant == 2:
            key = (out_degree - in_degree, out_degree, -in_degree, -vertex)
        else:
            key = (-vertex, out_degree, -in_degree, 0)
        if best_key is None or key > best_key:
            best_key = key
            best_vertex = vertex
    return best_vertex


def greedy_path(
    start: int,
    n: int,
    outgoing: list[set[int]],
    incoming: list[set[int]],
    variant: int,
) -> list[int]:
    used = bytearray(n + 1)
    used[start] = 1
    path = deque([start])

    while len(path) < n:
        tail_choice = choose_candidate(outgoing[path[-1]], used, outgoing, incoming, variant)
        head_choice = choose_candidate(incoming[path[0]], used, outgoing, incoming, variant)
        if tail_choice == 0 and head_choice == 0:
            break
        if tail_choice and head_choice:
            tail_key = (len(outgoing[tail_choice]), -len(incoming[tail_choice]), -tail_choice)
            head_key = (len(incoming[head_choice]), -len(outgoing[head_choice]), -head_choice)
            append_tail = tail_key >= head_key
        else:
            append_tail = tail_choice != 0
        if append_tail:
            used[tail_choice] = 1
            path.append(tail_choice)
        else:
            used[head_choice] = 1
            path.appendleft(head_choice)

    return list(path)


def heuristic_path(n: int, outgoing: list[set[int]], incoming: list[set[int]]) -> list[int]:
    vertex_order = sorted(
        range(1, n + 1),
        key=lambda vertex: (-(len(outgoing[vertex]) + len(incoming[vertex])), -len(outgoing[vertex]), vertex),
    )
    if n <= 300:
        starts = vertex_order[:24]
    else:
        starts = vertex_order[:24] + list(range(1, min(n, 8) + 1))

    best_path = [1]
    for start in dict.fromkeys(starts):
        for variant in range(4):
            path = greedy_path(start, n, outgoing, incoming, variant)
            if len(path) > len(best_path):
                best_path = path
                if len(best_path) == n:
                    return best_path
    return best_path


def main() -> int:
    n, _thresholds, outgoing, incoming = parse_input()
    path = dag_longest_path(n, outgoing, incoming)
    if path is None:
        path = heuristic_path(n, outgoing, incoming)
    if not path:
        path = [1]
    print(len(path))
    if len(path) != 1:
        print(" ".join(str(vertex) for vertex in path))
    else:
        print(path[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
