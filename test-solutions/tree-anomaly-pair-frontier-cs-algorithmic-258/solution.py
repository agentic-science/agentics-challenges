from __future__ import annotations

import sys


def read_nonempty_line() -> str | None:
    while True:
        line = sys.stdin.readline()
        if not line:
            return None
        line = line.strip()
        if line:
            return line


def ask(nodes: list[int]) -> tuple[int, int]:
    print("? " + str(len(nodes)) + " " + " ".join(map(str, nodes)), flush=True)
    line = read_nonempty_line()
    if line is None:
        raise EOFError("interactor closed while answering query")
    best, distance_sum = map(int, line.split())
    if best == -1 and distance_sum == -1:
        raise SystemExit(0)
    return best, distance_sum


def path_endpoints(adj: list[list[int]], on_path: set[int]) -> tuple[int, int]:
    endpoints = [
        node
        for node in on_path
        if sum(1 for nxt in adj[node] if nxt in on_path) <= 1
    ]
    if len(endpoints) >= 2:
        return endpoints[0], endpoints[1]
    ordered = sorted(on_path)
    return ordered[0], ordered[1]


def solve_case(n: int, edges: list[tuple[int, int]]) -> bool:
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    if n == 2:
        answer = (1, 2)
    else:
        distance_sums = [0] * (n + 1)
        for node in range(1, n + 1):
            _, distance_sums[node] = ask([node])
        minimum = min(distance_sums[1:])
        on_path = {node for node in range(1, n + 1) if distance_sums[node] == minimum}
        answer = path_endpoints(adj, on_path)

    print(f"! {answer[0]} {answer[1]}", flush=True)
    feedback = read_nonempty_line()
    return feedback == "Correct"


def main() -> int:
    line = read_nonempty_line()
    if line is None:
        return 0
    tests = int(line)
    for _ in range(tests):
        line = read_nonempty_line()
        if line is None:
            return 0
        n = int(line)
        edges = []
        for _ in range(n - 1):
            edge_line = read_nonempty_line()
            if edge_line is None:
                return 0
            u, v = map(int, edge_line.split())
            edges.append((u, v))
        if not solve_case(n, edges):
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
