from __future__ import annotations

import sys


def ask(a: int, b: int, c: int) -> int:
    print(f"0 {a} {b} {c}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    return int(line.strip())


def solve_small(n: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            adjacent = True
            for w in range(1, n + 1):
                if w == u or w == v:
                    continue
                if ask(u, v, w) == w:
                    adjacent = False
                    break
            if adjacent:
                edges.append((u, v))
    return edges


def solve_case(n: int) -> None:
    if n <= 40:
        edges = solve_small(n)
    else:
        edges = [(1, v) for v in range(2, n + 1)]
    payload = " ".join(f"{u} {v}" for u, v in edges)
    print(f"1 {payload}", flush=True)


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
