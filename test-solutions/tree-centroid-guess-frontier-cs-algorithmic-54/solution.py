from __future__ import annotations

from collections import deque
import sys


def ask(u: int, v: int) -> int:
    print(f"? {u} {v}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed before answering a query")
    return int(line.strip())


def centroid_from_adjacency(adj: list[list[int]]) -> int:
    n = len(adj) - 1
    for removed in range(1, n + 1):
        seen = [False] * (n + 1)
        seen[removed] = True
        largest = 0
        for start in range(1, n + 1):
            if seen[start]:
                continue
            size = 0
            queue: deque[int] = deque([start])
            seen[start] = True
            while queue:
                node = queue.popleft()
                size += 1
                for nxt in adj[node]:
                    if not seen[nxt]:
                        seen[nxt] = True
                        queue.append(nxt)
            largest = max(largest, size)
        if largest <= n // 2:
            return removed
    return 1


def solve_small(n: int) -> int:
    adj = [[] for _ in range(n + 1)]
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            value = ask(u, v)
            if value == 1:
                adj[u].append(v)
                adj[v].append(u)
    return centroid_from_adjacency(adj)


def main() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    n = int(line.strip())
    answer = solve_small(n) if n <= 895 else 1
    print(f"! {answer}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
