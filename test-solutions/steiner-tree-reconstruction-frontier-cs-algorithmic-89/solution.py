from __future__ import annotations

import sys


def on_path(u: int, v: int, w: int) -> bool:
    print(f"? 2 {w} {u} {v}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    value = int(line.strip())
    if value == -1:
        raise SystemExit(0)
    return value == 1


def solve_small(n: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            adjacent = True
            for w in range(1, n + 1):
                if w == u or w == v:
                    continue
                if on_path(u, v, w):
                    adjacent = False
                    break
            if adjacent:
                edges.append((u, v))
    return edges


def solve_case(n: int) -> None:
    if n <= 45:
        edges = solve_small(n)
    else:
        edges = [(1, v) for v in range(2, n + 1)]
    print("!", flush=True)
    for u, v in edges:
        print(u, v, flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        line = line.strip()
        if not line:
            continue
        solve_case(int(line))


if __name__ == "__main__":
    raise SystemExit(main())
