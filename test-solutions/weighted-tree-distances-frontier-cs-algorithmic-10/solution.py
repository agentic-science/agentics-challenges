from __future__ import annotations

import sys

MAX_EXACT_N = 120
MAX_STAR_DISTANCE_QUERIES = 4096


def read_nonempty() -> str | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        if line.strip():
            return line.strip()


def ask(u: int, v: int) -> int:
    print(f"? {u} {v}", flush=True)
    response = read_nonempty()
    if response is None:
        raise EOFError("interactor closed during distance query")
    return int(response)


def print_edges(edges: list[tuple[int, int, int]]) -> None:
    payload = ["!"]
    for u, v, weight in edges:
        payload.extend([str(u), str(v), str(weight)])
    print(" ".join(payload), flush=True)


def solve_exact(n: int) -> None:
    dist = [[0] * (n + 1) for _ in range(n + 1)]
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            value = ask(u, v)
            dist[u][v] = value
            dist[v][u] = value

    edges: list[tuple[int, int, int]] = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            direct = True
            for w in range(1, n + 1):
                if w != u and w != v and dist[u][v] == dist[u][w] + dist[w][v]:
                    direct = False
                    break
            if direct:
                edges.append((u, v, dist[u][v]))

    print_edges(edges[: max(0, n - 1)])


def solve_star_guess(n: int) -> None:
    edges: list[tuple[int, int, int]] = []
    query_budget = min(MAX_STAR_DISTANCE_QUERIES, max(0, n - 1))
    for offset, v in enumerate(range(2, n + 1), start=1):
        weight = ask(1, v) if offset <= query_budget else 1
        edges.append((1, v, max(1, weight)))
    print_edges(edges)


def solve_tree(n: int) -> None:
    if n <= MAX_EXACT_N:
        solve_exact(n)
    else:
        solve_star_guess(n)


def main() -> int:
    while True:
        line = read_nonempty()
        if line is None:
            return 0
        t = int(line)
        if t == 0:
            return 0
        for _ in range(t):
            n_line = read_nonempty()
            if n_line is None:
                return 0
            solve_tree(int(n_line))


if __name__ == "__main__":
    raise SystemExit(main())
