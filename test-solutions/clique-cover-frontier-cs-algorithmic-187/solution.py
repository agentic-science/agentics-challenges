from __future__ import annotations

import os
from pathlib import Path


def read_input() -> tuple[int, list[tuple[int, int]]]:
    text = (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")
    values = [int(token) for token in text.split()]
    if len(values) < 2:
        return 0, []
    n, m = values[:2]
    edges = []
    pos = 2
    for _ in range(m):
        if pos + 1 >= len(values):
            break
        u, v = values[pos], values[pos + 1]
        pos += 2
        if 1 <= u <= n and 1 <= v <= n and u != v:
            edges.append((u - 1, v - 1))
    return n, edges


def write_output(colors: list[int]) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(f"{color}\n" for color in colors), encoding="utf-8")


def dsatur_clique_cover(n: int, edges: list[tuple[int, int]]) -> list[int]:
    if n <= 0:
        return []

    full_mask = (1 << n) - 1
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    complement = [(~adj[v]) & full_mask & ~(1 << v) for v in range(n)]
    complement_degree = [mask.bit_count() for mask in complement]
    colors = [0] * n
    color_sets = [0]
    used_neighbor_colors = [0] * n
    saturation_degree = [0] * n
    uncolored = full_mask
    color_count = 0

    for _ in range(n):
        best = -1
        best_key = (-1, -1, 0)
        remaining = uncolored
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            key = (saturation_degree[vertex], complement_degree[vertex], -vertex)
            if key > best_key:
                best_key = key
                best = vertex
            remaining ^= bit

        color = 1
        while color <= color_count and (complement[best] & color_sets[color]):
            color += 1
        if color > color_count:
            color_count += 1
            color_sets.append(0)

        colors[best] = color
        color_sets[color] |= 1 << best
        uncolored &= ~(1 << best)

        neighbors = complement[best] & uncolored
        color_bit = 1 << color
        while neighbors:
            bit = neighbors & -neighbors
            vertex = bit.bit_length() - 1
            if not used_neighbor_colors[vertex] & color_bit:
                used_neighbor_colors[vertex] |= color_bit
                saturation_degree[vertex] += 1
            neighbors ^= bit

    relocate_to_lower_colors(colors, complement)
    return compress_colors(colors)


def relocate_to_lower_colors(colors: list[int], complement: list[int]) -> None:
    if not colors:
        return
    color_count = max(colors)
    color_sets = [0] * (color_count + 1)
    for vertex, color in enumerate(colors):
        color_sets[color] |= 1 << vertex

    changed = True
    while changed:
        changed = False
        for color in range(color_count, 1, -1):
            members = color_sets[color]
            while members:
                bit = members & -members
                vertex = bit.bit_length() - 1
                for target in range(1, color):
                    if complement[vertex] & color_sets[target]:
                        continue
                    color_sets[color] &= ~bit
                    color_sets[target] |= bit
                    colors[vertex] = target
                    changed = True
                    break
                members ^= bit


def compress_colors(colors: list[int]) -> list[int]:
    remap: dict[int, int] = {}
    next_color = 1
    result = []
    for color in colors:
        if color not in remap:
            remap[color] = next_color
            next_color += 1
        result.append(remap[color])
    return result


def main() -> int:
    n, edges = read_input()
    write_output(dsatur_clique_cover(n, edges))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
