from __future__ import annotations

import os
from pathlib import Path
import random
import time


HEIGHT = 8
WIDTH = 14
CELLS = HEIGHT * WIDTH
SEARCH_CAP = 2000


NEIGHBOR_MASKS: list[int] = []
for row in range(HEIGHT):
    for col in range(WIDTH):
        mask = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = row + dr
                nc = col + dc
                if 0 <= nr < HEIGHT and 0 <= nc < WIDTH:
                    mask |= 1 << (nr * WIDTH + nc)
        NEIGHBOR_MASKS.append(mask)

NUMBER_DIGITS = [()] + [tuple(map(int, str(value))) for value in range(1, SEARCH_CAP + 1)]


def write_output(rows: list[str]) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")


def digit_masks(grid: list[int]) -> list[int]:
    masks = [0] * 10
    for idx, digit in enumerate(grid):
        masks[digit] |= 1 << idx
    return masks


def can_read(digits: tuple[int, ...], masks: list[int]) -> bool:
    frontier = masks[digits[0]]
    if frontier == 0:
        return False
    for digit in digits[1:]:
        reachable = 0
        bits = frontier
        while bits:
            bit = bits & -bits
            reachable |= NEIGHBOR_MASKS[bit.bit_length() - 1]
            bits ^= bit
        frontier = reachable & masks[digit]
        if frontier == 0:
            return False
    return True


def prefix_score(grid: list[int], cap: int = SEARCH_CAP) -> int:
    masks = digit_masks(grid)
    for digit in range(1, 10):
        if masks[digit] == 0:
            return digit - 1
    for value in range(1, cap + 1):
        if not can_read(NUMBER_DIGITS[value], masks):
            return value - 1
    return cap


def champernowne_grid() -> list[int]:
    stream = "".join(str(value) for value in range(1, 10000))
    grid = [0] * CELLS
    cursor = 0
    for row in range(HEIGHT):
        cols = range(WIDTH) if row % 2 == 0 else range(WIDTH - 1, -1, -1)
        for col in cols:
            grid[row * WIDTH + col] = int(stream[cursor])
            cursor += 1
    return grid


def random_grid(rng: random.Random) -> list[int]:
    grid = [rng.randrange(10) for _ in range(CELLS)]
    for digit in range(10):
        grid[digit] = digit
    rng.shuffle(grid)
    return grid


def improve(seed: list[int], rng: random.Random, deadline: float) -> tuple[int, list[int]]:
    current = seed[:]
    current_score = prefix_score(current)
    best_score = current_score
    best = current[:]

    while time.monotonic() < deadline:
        idx = rng.randrange(CELLS)
        old = current[idx]
        new = rng.randrange(10)
        if new == old:
            continue
        current[idx] = new
        trial_cap = min(SEARCH_CAP, max(current_score + 180, 260))
        trial_score = prefix_score(current, trial_cap)
        if trial_score >= current_score:
            current_score = prefix_score(current, SEARCH_CAP) if trial_score == trial_cap else trial_score
            if current_score > best_score:
                best_score = current_score
                best = current[:]
        else:
            current[idx] = old

    return best_score, best


def main() -> int:
    rng = random.Random(110_313)
    deadline = time.monotonic() + 1.7
    best_score = -1
    best_grid = champernowne_grid()

    seeds = [best_grid, random_grid(rng), random_grid(rng), random_grid(rng)]
    for seed in seeds:
        score, grid = improve(seed, rng, deadline)
        if score > best_score:
            best_score = score
            best_grid = grid
        if time.monotonic() >= deadline:
            break

    rows = [
        "".join(str(best_grid[row * WIDTH + col]) for col in range(WIDTH))
        for row in range(HEIGHT)
    ]
    write_output(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
