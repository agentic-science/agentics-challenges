from __future__ import annotations

import math
import os
from pathlib import Path


Point = tuple[float, float, float]
SHRINK = 1.0 - 1e-12


def read_input() -> str:
    return (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")


def write_output(text: str) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def normalize(point: Point) -> Point:
    x, y, z = point
    norm = math.sqrt(x * x + y * y + z * z)
    if norm == 0.0:
        return (SHRINK, 0.0, 0.0)
    scale = SHRINK / norm
    return (x * scale, y * scale, z * scale)


def special_points(n: int) -> list[Point]:
    if n == 2:
        return [(0.0, 0.0, SHRINK), (0.0, 0.0, -SHRINK)]
    if n == 3:
        return [normalize((math.cos(2.0 * math.pi * k / 3.0), math.sin(2.0 * math.pi * k / 3.0), 0.0)) for k in range(3)]
    if n == 4:
        s = 1.0 / math.sqrt(3.0)
        return [normalize(p) for p in [(s, s, s), (s, -s, -s), (-s, s, -s), (-s, -s, s)]]
    if n == 6:
        return [
            (SHRINK, 0.0, 0.0),
            (-SHRINK, 0.0, 0.0),
            (0.0, SHRINK, 0.0),
            (0.0, -SHRINK, 0.0),
            (0.0, 0.0, SHRINK),
            (0.0, 0.0, -SHRINK),
        ]
    return []


def fibonacci_sphere(n: int) -> list[Point]:
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    points: list[Point] = []
    for k in range(n):
        z = 1.0 - (2.0 * k + 1.0) / n
        radius = math.sqrt(max(0.0, 1.0 - z * z))
        theta = golden_angle * k
        points.append(normalize((math.cos(theta) * radius, math.sin(theta) * radius, z)))
    return points


def min_distance(points: list[Point]) -> float:
    best2 = float("inf")
    for i, (x1, y1, z1) in enumerate(points):
        for x2, y2, z2 in points[i + 1:]:
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            best2 = min(best2, dx * dx + dy * dy + dz * dz)
    return math.sqrt(best2)


def main() -> int:
    tokens = read_input().split()
    n = int(tokens[0]) if tokens else 2
    points = special_points(n) or fibonacci_sphere(n)
    lines = [f"{min_distance(points):.15f}"]
    lines.extend(f"{x:.15f} {y:.15f} {z:.15f}" for x, y, z in points)
    write_output("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
