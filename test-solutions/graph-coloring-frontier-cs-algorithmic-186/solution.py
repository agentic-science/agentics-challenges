from __future__ import annotations

import os
from pathlib import Path


def read_input() -> tuple[int, list[set[int]]]:
    text = (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")
    data = [int(token) for token in text.split()]
    if not data:
        return 0, []
    n, m = data[0], data[1]
    graph = [set() for _ in range(n)]
    pos = 2
    for _ in range(m):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        if u == v:
            continue
        graph[u].add(v)
        graph[v].add(u)
    return n, graph


def write_colors(colors: list[int]) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(f"{color}\n" for color in colors), encoding="utf-8")


def dsatur_coloring(graph: list[set[int]]) -> list[int]:
    n = len(graph)
    colors = [0] * n
    neighbor_colors = [set() for _ in range(n)]
    uncolored = set(range(n))
    degrees = [len(neighbors) for neighbors in graph]

    while uncolored:
        vertex = max(uncolored, key=lambda v: (len(neighbor_colors[v]), degrees[v], -v))
        color = 1
        while color in neighbor_colors[vertex]:
            color += 1
        colors[vertex] = color
        uncolored.remove(vertex)
        for neighbor in graph[vertex]:
            if colors[neighbor] == 0:
                neighbor_colors[neighbor].add(color)

    return colors


def reduce_colors(graph: list[set[int]], colors: list[int]) -> list[int]:
    degrees = [len(neighbors) for neighbors in graph]
    for _ in range(3):
        changed = False
        order = sorted(range(len(colors)), key=lambda v: (-colors[v], -degrees[v], v))
        for vertex in order:
            blocked = {colors[neighbor] for neighbor in graph[vertex]}
            for color in range(1, colors[vertex]):
                if color not in blocked:
                    colors[vertex] = color
                    changed = True
                    break
        if not changed:
            break
    return colors


def main() -> int:
    _n, graph = read_input()
    colors = reduce_colors(graph, dsatur_coloring(graph)) if graph else []
    write_colors(colors)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
