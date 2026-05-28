from __future__ import annotations

import sys

N = 400
M = 5 * (N - 1)


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if self.size[left_root] < self.size[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        self.size[left_root] += self.size[right_root]
        return True


def read_pair() -> tuple[int, int] | None:
    line = sys.stdin.readline()
    if not line:
        return None
    a, b = map(int, line.split())
    return a, b


def main() -> int:
    for _ in range(N):
        if read_pair() is None:
            return 0

    edges: list[tuple[int, int]] = []
    for _ in range(M):
        pair = read_pair()
        if pair is None:
            return 0
        edges.append(pair)

    dsu = DSU(N)
    for u, v in edges:
        cost_line = sys.stdin.readline()
        if not cost_line:
            return 0
        take = 1 if dsu.union(u, v) else 0
        print(take, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
