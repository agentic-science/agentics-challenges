from __future__ import annotations

import os
from pathlib import Path


def read_input() -> str:
    return (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")


def write_output(text: str) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def greedy_independent_set(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adjacency: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u == v:
            continue
        a = u - 1
        b = v - 1
        if 0 <= a < n and 0 <= b < n:
            adjacency[a].add(b)
            adjacency[b].add(a)

    selected = [0] * n
    blocked = bytearray(n)
    order = sorted(range(n), key=lambda vertex: (len(adjacency[vertex]), vertex))
    for vertex in order:
        if blocked[vertex]:
            continue
        selected[vertex] = 1
        blocked[vertex] = 1
        for neighbor in adjacency[vertex]:
            blocked[neighbor] = 1
    return selected


def main() -> int:
    data = [int(token) for token in read_input().split()]
    if len(data) < 2:
        write_output("")
        return 0

    n, m = data[0], data[1]
    raw_edges = data[2:]
    edges = [(raw_edges[2 * i], raw_edges[2 * i + 1]) for i in range(min(m, len(raw_edges) // 2))]
    solution = greedy_independent_set(n, edges)
    write_output("\n".join(str(value) for value in solution) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
