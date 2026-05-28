from __future__ import annotations

from collections import deque
import sys


def read_line() -> str:
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed")
    return line.strip()


def ask(nodes: list[int]) -> int:
    print(f"? 1 {len(nodes)} " + " ".join(map(str, nodes)), flush=True)
    return int(read_line())


def toggle(node: int) -> None:
    print(f"? 2 {node}", flush=True)


def parents_from(root: int, graph: list[list[int]]) -> list[int]:
    parent = [0] * len(graph)
    parent[root] = -1
    queue: deque[int] = deque([root])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if parent[nxt] == 0:
                parent[nxt] = node
                queue.append(nxt)
    return parent


def solve_case(n: int, edges: list[tuple[int, int]]) -> None:
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    current = [0] + [ask([node]) for node in range(1, n + 1)]
    total = sum(current)
    all_nodes = list(range(1, n + 1))
    candidates = [node for node in all_nodes if abs(current[node]) == 1] or all_nodes
    root = candidates[0]

    for node in candidates:
        toggle(node)
        new_total = ask(all_nodes)
        if abs(new_total - total) == 2 * n:
            root = node
            total = new_total
            break
        total = new_total

    sums = [0] + [ask([node]) for node in range(1, n + 1)]
    parent = parents_from(root, graph)
    values = [0] * (n + 1)
    values[root] = 1 if sums[root] > 0 else -1
    order = [root]
    for node in order:
        for nxt in graph[node]:
            if parent[nxt] == node:
                diff = sums[nxt] - sums[node]
                values[nxt] = 1 if diff > 0 else -1
                order.append(nxt)

    print("! " + " ".join(str(values[node]) for node in range(1, n + 1)), flush=True)


def main() -> int:
    try:
        t = int(read_line())
        for _ in range(t):
            n = int(read_line())
            edges = [tuple(map(int, read_line().split())) for _ in range(max(0, n - 1))]
            solve_case(n, edges)
    except EOFError:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
