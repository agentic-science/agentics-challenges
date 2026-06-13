from __future__ import annotations

import os
from pathlib import Path

MOVES = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))


def read_input() -> str:
    return (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")


def write_output(text: str) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def warnsdorff_path(n: int, start_row: int, start_col: int) -> list[tuple[int, int]]:
    total = n * n
    visited = bytearray(total)
    center = (n - 1) / 2.0
    row = start_row - 1
    col = start_col - 1
    path: list[tuple[int, int]] = []

    def index(r: int, c: int) -> int:
        return r * n + c

    for _ in range(total):
        path.append((row + 1, col + 1))
        visited[index(row, col)] = 1

        best_cell: tuple[int, int] | None = None
        best_key: tuple[int, float, int, int] | None = None
        for dr, dc in MOVES:
            nr = row + dr
            nc = col + dc
            if nr < 0 or nr >= n or nc < 0 or nc >= n or visited[index(nr, nc)]:
                continue

            onward_degree = 0
            for adr, adc in MOVES:
                ar = nr + adr
                ac = nc + adc
                if 0 <= ar < n and 0 <= ac < n and not visited[index(ar, ac)]:
                    onward_degree += 1
            distance_from_center = abs(nr - center) + abs(nc - center)
            key = (onward_degree, -distance_from_center, nr, nc)
            if best_key is None or key < best_key:
                best_key = key
                best_cell = (nr, nc)

        if best_cell is None:
            break
        row, col = best_cell

    return path


def main() -> int:
    data = [int(token) for token in read_input().split()]
    if len(data) < 3:
        write_output("0\n")
        return 0

    n, row, col = data[:3]
    path = warnsdorff_path(n, row, col)
    lines = [str(len(path))]
    lines.extend(f"{r} {c}" for r, c in path)
    write_output("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
