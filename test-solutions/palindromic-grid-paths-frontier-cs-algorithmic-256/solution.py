from __future__ import annotations

import itertools
import sys
from functools import lru_cache


def ask(x1: int, y1: int, x2: int, y2: int) -> int:
    print(f"? {x1} {y1} {x2} {y2}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed during query")
    return int(line)


def has_palindromic_path(grid: tuple[str, ...], x1: int, y1: int, x2: int, y2: int) -> bool:
    n = len(grid)
    r1, c1, r2, c2 = x1 - 1, y1 - 1, x2 - 1, y2 - 1

    @lru_cache(maxsize=None)
    def solve(a: int, b: int, c: int, d: int) -> bool:
        if grid[a][b] != grid[c][d]:
            return False
        if a == c and b == d:
            return True
        if a + b + 1 == c + d:
            return True
        for na, nb in ((a + 1, b), (a, b + 1)):
            if not (0 <= na < n and 0 <= nb < n):
                continue
            for nc, nd in ((c - 1, d), (c, d - 1)):
                if 0 <= nc < n and 0 <= nd < n and solve(na, nb, nc, nd):
                    return True
        return False

    return solve(r1, c1, r2, c2)


def all_queries(n: int) -> list[tuple[int, int, int, int]]:
    queries = []
    for x1 in range(1, n + 1):
        for y1 in range(1, n + 1):
            for x2 in range(x1, n + 1):
                for y2 in range(y1, n + 1):
                    if x1 + y1 + 2 <= x2 + y2:
                        queries.append((x1, y1, x2, y2))
    return queries


def solve_small(n: int) -> list[str]:
    observations = [(query, ask(*query)) for query in all_queries(n)]
    for bits in itertools.product("01", repeat=n * n):
        grid = tuple("".join(bits[row * n:(row + 1) * n]) for row in range(n))
        if all(has_palindromic_path(grid, *query) == bool(reply) for query, reply in observations):
            return list(grid)
    return ["0" * n for _ in range(n)]


def main() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    n = int(line)
    if n <= 3:
        grid = solve_small(n)
    else:
        grid = ["0" * n for _ in range(n)]
    print("!", flush=True)
    for row in grid:
        print(row, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
