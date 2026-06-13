from __future__ import annotations

import sys


def parse_points(tokens: list[str]) -> tuple[int, int, list[tuple[int, int]]]:
    if len(tokens) < 2:
        return 0, 0, []
    n = int(tokens[0])
    m = int(tokens[1])
    coords = [int(value) for value in tokens[2:]]
    point_count = min(len(coords) // 2, m)
    points = [(coords[2 * i], coords[2 * i + 1]) for i in range(point_count)]
    return n, m, points


def route(points: list[tuple[int, int]]) -> list[tuple[str, str]]:
    if not points:
        return []

    r, c = points[0]
    actions: list[tuple[str, str]] = []
    for tr, tc in points[1:]:
        while r > tr:
            actions.append(("M", "U"))
            r -= 1
        while r < tr:
            actions.append(("M", "D"))
            r += 1
        while c > tc:
            actions.append(("M", "L"))
            c -= 1
        while c < tc:
            actions.append(("M", "R"))
            c += 1
    return actions


def main() -> int:
    _n, _m, points = parse_points(sys.stdin.read().split())
    sys.stdout.write("".join(f"{action} {direction}\n" for action, direction in route(points)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
