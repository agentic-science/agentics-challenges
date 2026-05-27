from __future__ import annotations

import sys


def ask(bits: list[int]) -> int:
    print("0 " + " ".join(str(bit) for bit in bits), flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactive evaluator closed before replying")
    return int(line.strip())


def solve_case(n: int, m: int, edges: list[tuple[int, int]]) -> None:
    path_edge = [-1] * max(0, n - 1)
    for index, (u, v) in enumerate(edges):
        if v == u + 1 and 0 <= u < n - 1:
            path_edge[u] = index
    if len(path_edge) != n - 1 or any(index < 0 for index in path_edge):
        print("1 0 1", flush=True)
        return

    increasing = [0] * m
    if ask(increasing) == 1:
        inside: list[int] = []
        for edge_pos, edge_index in enumerate(path_edge):
            bits = [0] * m
            bits[edge_index] = 1
            if ask(bits) == 0:
                inside.append(edge_pos)
        if not inside:
            print("1 0 1", flush=True)
            return
        print(f"1 {min(inside)} {max(inside) + 1}", flush=True)
        return

    decreasing = [1] * m
    inside = []
    for edge_pos, edge_index in enumerate(path_edge):
        bits = [1] * m
        bits[edge_index] = 0
        if ask(bits) == 0:
            inside.append(edge_pos)
    if not inside:
        print("1 1 0", flush=True)
        return
    print(f"1 {max(inside) + 1} {min(inside)}", flush=True)


def main() -> None:
    while True:
        first = sys.stdin.readline()
        if first == "":
            return
        if not first.strip():
            continue
        n, m = map(int, first.split())
        edges = [tuple(map(int, sys.stdin.readline().split())) for _ in range(m)]
        solve_case(n, m, edges)


if __name__ == "__main__":
    main()
