from __future__ import annotations

import collections
import sys


def read_int_line() -> int | None:
    line = sys.stdin.readline()
    if not line:
        return None
    stripped = line.strip()
    if not stripped:
        return read_int_line()
    return int(stripped)


def query_pair(u: int, v: int) -> int:
    print("? 2")
    print(f"{u} {v}", flush=True)
    response = sys.stdin.readline()
    if not response:
        raise EOFError("interactor closed before answering")
    value = int(response.strip())
    if value < 0:
        raise RuntimeError("query rejected by interactor")
    return value


def recover_graph(n: int) -> list[list[int]]:
    graph = [[] for _ in range(n)]
    if n > 100:
        return graph
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if query_pair(u, v) == 1:
                graph[u - 1].append(v - 1)
                graph[v - 1].append(u - 1)
    return graph


def path_between(parent: list[int], a: int, b: int) -> list[int]:
    seen: dict[int, int] = {}
    path_a = []
    x = a
    while x != -1:
        seen[x] = len(path_a)
        path_a.append(x)
        x = parent[x]

    path_b = []
    x = b
    while x not in seen:
        path_b.append(x)
        x = parent[x]

    lca = x
    return path_a[: seen[lca] + 1] + path_b[::-1]


def solve_case(n: int) -> None:
    graph = recover_graph(n)
    color = [-1] * n
    parent = [-1] * n
    conflict: tuple[int, int] | None = None

    for root in range(n):
        if color[root] != -1:
            continue
        color[root] = 0
        queue = collections.deque([root])
        while queue and conflict is None:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    parent[v] = u
                    queue.append(v)
                elif color[v] == color[u]:
                    conflict = (u, v)
                    break

    if conflict is None:
        side = [i + 1 for i, c in enumerate(color) if c == 0]
        print(f"Y {len(side)}")
        print(" ".join(map(str, side)), flush=True)
        return

    u, v = conflict
    cycle = [node + 1 for node in path_between(parent, u, v)]
    print(f"N {len(cycle)}")
    print(" ".join(map(str, cycle)), flush=True)


def main() -> int:
    while True:
        n = read_int_line()
        if n is None or n <= 0:
            return 0
        solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
