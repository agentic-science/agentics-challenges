from __future__ import annotations

import sys
from collections import Counter

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def distance_to_wall(grid: list[str], row: int, col: int, direction: int) -> int:
    rows, cols = len(grid), len(grid[0])
    dr, dc = DIRECTIONS[direction]
    dist = 0
    row += dr
    col += dc
    while 0 <= row < rows and 0 <= col < cols and grid[row][col] == ".":
        dist += 1
        row += dr
        col += dc
    return dist


def apply_action(state: tuple[int, int, int], action: str) -> tuple[int, int, int]:
    row, col, direction = state
    if action == "left":
        return row, col, (direction + 3) % 4
    if action == "right":
        return row, col, (direction + 1) % 4
    dr, dc = DIRECTIONS[direction]
    return row + dr, col + dc, direction


def step_is_safe(grid: list[str], states: list[tuple[int, int, int]]) -> bool:
    rows, cols = len(grid), len(grid[0])
    for row, col, direction in states:
        dr, dc = DIRECTIONS[direction]
        nr, nc = row + dr, col + dc
        if not (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "."):
            return False
    return True


def choose_action(grid: list[str], states: list[tuple[int, int, int]]) -> str | None:
    choices = ["left", "right"]
    if step_is_safe(grid, states):
        choices.append("step")

    best: tuple[int, int, str] | None = None
    for action in choices:
        next_states = [apply_action(state, action) for state in states]
        buckets = Counter(distance_to_wall(grid, *state) for state in next_states)
        score = (max(buckets.values()), len(set(next_states)), action)
        if best is None or score < best:
            best = score
    return None if best is None else best[2]


def solve_case(first: str) -> bool:
    parts = first.split()
    if len(parts) != 2:
        return False
    rows, cols = map(int, parts)
    grid = [sys.stdin.readline().strip() for _ in range(rows)]
    states = [
        (row, col, direction)
        for row in range(rows)
        for col in range(cols)
        if grid[row][col] == "."
        for direction in range(4)
    ]

    for _ in range(1000):
        line = sys.stdin.readline()
        if not line:
            return False
        observed = int(line.strip())
        if observed < 0:
            return False
        states = [state for state in states if distance_to_wall(grid, *state) == observed]
        positions = {(row, col) for row, col, _direction in states}
        if len(positions) == 1:
            row, col = next(iter(positions))
            print(f"yes {row + 1} {col + 1}", flush=True)
            return True
        action = choose_action(grid, states)
        if action is None:
            print("no", flush=True)
            return True
        print(action, flush=True)
        states = [apply_action(state, action) for state in states]

    print("no", flush=True)
    return True


def main() -> int:
    while True:
        first = sys.stdin.readline()
        if not first:
            return 0
        first = first.strip()
        if not first:
            continue
        if not solve_case(first):
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
