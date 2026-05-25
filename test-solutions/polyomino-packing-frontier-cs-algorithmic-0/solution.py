from __future__ import annotations

import sys


def parse_shapes(tokens: list[int]) -> list[list[tuple[int, int]]]:
    if not tokens:
        raise ValueError("missing n")
    index = 0
    n = tokens[index]
    index += 1
    shapes: list[list[tuple[int, int]]] = []
    for _ in range(n):
        k = tokens[index]
        index += 1
        cells: list[tuple[int, int]] = []
        for _ in range(k):
            cells.append((tokens[index], tokens[index + 1]))
            index += 2
        shapes.append(cells)
    return shapes


def main() -> int:
    tokens = [int(token) for token in sys.stdin.read().split()]
    shapes = parse_shapes(tokens)
    placements: list[tuple[int, int, int, int]] = []
    offset_x = 0
    height = 1

    for cells in shapes:
        xs = [x for x, _y in cells]
        ys = [y for _x, y in cells]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x + 1
        piece_height = max_y - min_y + 1
        placements.append((offset_x - min_x, -min_y, 0, 0))
        offset_x += width
        height = max(height, piece_height)

    print(max(1, offset_x), height)
    for placement in placements:
        print(*placement)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
