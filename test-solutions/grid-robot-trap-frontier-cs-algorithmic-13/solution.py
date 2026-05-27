from __future__ import annotations

from collections import deque
import sys

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
LIMIT = 3000


def read_pair() -> tuple[int, int] | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        if line.strip():
            a, b = (int(part) for part in line.split()[:2])
            return a, b


def source_next(
    pos: tuple[int, int],
    mask: int,
    mark: tuple[int, int],
    cells: list[tuple[int, int]],
    cell_to_index: dict[tuple[int, int], int],
) -> tuple[tuple[int, int], int] | None:
    if mark not in cell_to_index:
        return None
    next_mask = mask | (1 << cell_to_index[mark])
    black = [cell for i, cell in enumerate(cells) if (next_mask >> i) & 1]
    candidates: list[tuple[int, int]] = []
    for dx, dy in DIRS:
        candidate = (pos[0] + dx, pos[1] + dy)
        if candidate[0] < 1 or candidate[1] < 1:
            continue
        if candidate in cell_to_index:
            if not ((next_mask >> cell_to_index[candidate]) & 1):
                candidates.append(candidate)
        else:
            candidates.append(candidate)
    if not candidates:
        return (0, 0), next_mask
    if len(candidates) == 1:
        return candidates[0], next_mask

    def influence(candidate: tuple[int, int]) -> float:
        return sum(1.0 / (abs(candidate[0] - x) + abs(candidate[1] - y)) for x, y in black)

    return min(candidates, key=influence), next_mask


def find_corner_plan(start: tuple[int, int]) -> list[tuple[int, int]]:
    cells = [(x, y) for x in range(1, 6) for y in range(1, 6)]
    cell_to_index = {cell: index for index, cell in enumerate(cells)}
    if start not in cell_to_index:
        return []
    queue = deque([(start, 0)])
    parent: dict[tuple[tuple[int, int], int], tuple[tuple[tuple[int, int], int] | None, tuple[int, int] | None]] = {
        (start, 0): (None, None)
    }
    depth: dict[tuple[tuple[int, int], int], int] = {(start, 0): 0}
    while queue:
        pos, mask = queue.popleft()
        if depth[(pos, mask)] >= 8:
            continue
        for mark in cells:
            next_state = source_next(pos, mask, mark, cells, cell_to_index)
            if next_state is None:
                continue
            next_pos, next_mask = next_state
            if next_pos == (0, 0):
                path = [mark]
                cur = (pos, mask)
                while parent[cur][0] is not None:
                    prev, prev_mark = parent[cur]
                    assert prev is not None and prev_mark is not None
                    path.append(prev_mark)
                    cur = prev
                return list(reversed(path))
            if next_pos not in cell_to_index:
                continue
            key = (next_pos, next_mask)
            if key not in parent:
                parent[key] = ((pos, mask), mark)
                depth[key] = depth[(pos, mask)] + 1
                queue.append(key)
    return []


def play_mark(mark: tuple[int, int]) -> tuple[int, int] | None:
    print(f"{mark[0]} {mark[1]}", flush=True)
    return read_pair()


def solve_case(start: tuple[int, int]) -> None:
    pos = start
    for mark in find_corner_plan(start):
        response = play_mark(mark)
        if response is None or response == (0, 0):
            return
        pos = response

    for _ in range(LIMIT):
        if pos[0] == 1:
            mark = (2, min(LIMIT, pos[1]))
        elif pos[1] == 1:
            mark = (min(LIMIT, pos[0]), 2)
        else:
            mark = (max(1, pos[0] - 1), max(1, pos[1] - 1))
        response = play_mark(mark)
        if response is None or response == (0, 0):
            return
        pos = response


def main() -> int:
    while True:
        start = read_pair()
        if start is None or start == (0, 0):
            return 0
        solve_case(start)


if __name__ == "__main__":
    raise SystemExit(main())
