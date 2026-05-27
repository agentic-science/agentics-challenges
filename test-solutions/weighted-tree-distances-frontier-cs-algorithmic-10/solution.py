from __future__ import annotations

import sys


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


def solve_tree(n: int) -> None:
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

    payload = ["!"]
    for u, v, weight in edges[: max(0, n - 1)]:
        payload.extend([str(u), str(v), str(weight)])
    print(" ".join(payload), flush=True)


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
