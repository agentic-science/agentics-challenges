from __future__ import annotations

import sys


def is_subsequence(needle: list[int], haystack: list[int]) -> bool:
    pos = 0
    for value in haystack:
        if pos < len(needle) and needle[pos] == value:
            pos += 1
    return pos == len(needle)


def row_cells(row: int, start_col: int, left: int, right: int) -> list[tuple[int, int]]:
    if start_col == left:
        return [(row, col) for col in range(left, right + 1)]
    return [(row, col) for col in range(right, left - 1, -1)]


def append_segment(path: list[tuple[int, int]], rows: list[int], start_col: int, left: int, right: int) -> int:
    current_col = start_col
    for row in rows:
        cells = row_cells(row, current_col, left, right)
        path.extend(cells)
        current_col = cells[-1][1]
    return current_col


def connect_outside(
    path: list[tuple[int, int]],
    target_row: int,
    current_col: int,
    left: int,
    right: int,
    m: int,
) -> int | None:
    if current_col == right and right < m:
        outside_col = right + 1
        entry_col = right
    elif current_col == left and left > 1:
        outside_col = left - 1
        entry_col = left
    else:
        return None

    row = path[-1][0]
    path.append((row, outside_col))
    step = 1 if target_row > row else -1
    while row != target_row:
        row += step
        path.append((row, outside_col))
    return entry_col


def build_path_for_order(
    n: int,
    m: int,
    left: int,
    right: int,
    sx: int,
    sy: int,
    first: list[int],
    second: list[int],
) -> list[tuple[int, int]] | None:
    if not (1 <= sx <= n and sy == left and left <= right <= m):
        return None

    path: list[tuple[int, int]] = []
    current_col = append_segment(path, first, left, left, right)
    if second:
        entry_col = connect_outside(path, second[0], current_col, left, right, m)
        if entry_col is None:
            return None
        append_segment(path, second, entry_col, left, right)
    return path


def candidate_paths(
    n: int,
    m: int,
    left: int,
    right: int,
    sx: int,
    sy: int,
    q: list[int],
) -> list[list[tuple[int, int]]]:
    candidates: list[list[tuple[int, int]]] = []
    orders = [
        (list(range(sx, n + 1)), list(range(sx - 1, 0, -1))),
        (list(range(sx, 0, -1)), list(range(sx + 1, n + 1))),
    ]
    for first, second in orders:
        order = first + second
        if not is_subsequence(q, order):
            continue
        path = build_path_for_order(n, m, left, right, sx, sy, first, second)
        if path is not None:
            candidates.append(path)
    return candidates


def main() -> int:
    data = [int(token) for token in sys.stdin.read().split()]
    if len(data) < 8:
        return 0
    n, m, left, right, sx, sy, lq, _score_hint = data[:8]
    q = data[8:8 + lq]
    paths = candidate_paths(n, m, left, right, sx, sy, q)
    if not paths:
        print("NO")
        return 0

    path = min(paths, key=len)
    print("YES")
    print(len(path))
    for row, col in path:
        print(row, col)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
