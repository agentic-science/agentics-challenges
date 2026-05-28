from __future__ import annotations

import sys
import select
import time


N = 100


def query(a: int, b: int, c: int) -> int:
    print(f"? {a} {b} {c}", flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], 30.0)
    if not ready:
        raise EOFError
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    return int(line.strip())


def build_graph() -> list[list[int]]:
    q1: dict[tuple[int, int], int] = {}
    q2: dict[tuple[int, int], int] = {}
    for a in range(2, N + 1):
        for b in range(a + 1, N + 1):
            q1[(a, b)] = query(1, a, b)
    for a in range(3, N + 1):
        for b in range(a + 1, N + 1):
            q2[(a, b)] = query(2, a, b)

    d: dict[int, int] = {}
    d[3] = (q1[(3, 4)] - q2[(3, 4)] + q1[(3, 5)] - q2[(3, 5)] - q1[(4, 5)] + q2[(4, 5)]) // 2
    for vertex in range(4, N + 1):
        d[vertex] = q1[(3, vertex)] - q2[(3, vertex)] - d[3]

    for edge_12 in (0, 1):
        adj = [[0 for _ in range(N)] for _ in range(N)]
        adj[0][1] = adj[1][0] = edge_12
        ok = True
        for vertex in range(3, N + 1):
            total = q1[(2, vertex)] - edge_12
            a = total + d[vertex]
            b = total - d[vertex]
            if a % 2 or b % 2:
                ok = False
                break
            edge_1v = a // 2
            edge_2v = b // 2
            if edge_1v not in (0, 1) or edge_2v not in (0, 1):
                ok = False
                break
            adj[0][vertex - 1] = adj[vertex - 1][0] = edge_1v
            adj[1][vertex - 1] = adj[vertex - 1][1] = edge_2v
        if not ok:
            continue
        for a in range(3, N + 1):
            for b in range(a + 1, N + 1):
                edge = q1[(a, b)] - adj[0][a - 1] - adj[0][b - 1]
                if edge not in (0, 1):
                    ok = False
                    break
                adj[a - 1][b - 1] = adj[b - 1][a - 1] = edge
            if not ok:
                break
        if ok:
            return adj
    return [[0 for _ in range(N)] for _ in range(N)]


def main() -> int:
    while True:
        try:
            adj = build_graph()
        except EOFError:
            return 0
        print("!", flush=True)
        for row in adj:
            print("".join(str(value) for value in row), flush=True)
        time.sleep(0.5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
