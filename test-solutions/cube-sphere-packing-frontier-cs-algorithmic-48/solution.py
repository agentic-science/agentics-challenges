from __future__ import annotations

import math
import sys


def ceil_cuberoot(value: int) -> int:
    root = max(1, round(value ** (1.0 / 3.0)))
    while root**3 < value:
        root += 1
    while root > 1 and (root - 1) ** 3 >= value:
        root -= 1
    return root


def compact_prefix(points: list[tuple[int, int, int]], count: int) -> list[tuple[int, int, int]]:
    mins = [min(point[axis] for point in points) for axis in range(3)]
    maxs = [max(point[axis] for point in points) for axis in range(3)]
    center = tuple((mins[axis] + maxs[axis]) / 2.0 for axis in range(3))
    points.sort(
        key=lambda point: (
            max(abs(point[axis] - center[axis]) for axis in range(3)),
            sum((point[axis] - center[axis]) ** 2 for axis in range(3)),
            point,
        )
    )
    return points[:count]


def scaled_candidate(
    points: list[tuple[int, int, int]],
    count: int,
    lattice_distance: float,
) -> tuple[float, list[tuple[float, float, float]]]:
    selected = compact_prefix(points, count)
    if count == 1:
        return 0.5, [(0.5, 0.5, 0.5)]

    mins = [min(point[axis] for point in selected) for axis in range(3)]
    maxs = [max(point[axis] for point in selected) for axis in range(3)]
    spans = [maxs[axis] - mins[axis] for axis in range(3)]
    max_span = max(spans)
    if max_span <= 0:
        return 0.0, [(0.5, 0.5, 0.5) for _ in selected]

    scale = 1.0 / (max_span + lattice_distance)
    radius = 0.5 * lattice_distance * scale
    offsets = [radius + 0.5 * (max_span - spans[axis]) * scale for axis in range(3)]
    coordinates = [
        tuple((point[axis] - mins[axis]) * scale + offsets[axis] for axis in range(3))
        for point in selected
    ]
    return radius, coordinates


def simple_cubic_candidate(count: int) -> tuple[float, list[tuple[float, float, float]]]:
    side = ceil_cuberoot(count)
    points = [(x, y, z) for x in range(side) for y in range(side) for z in range(side)]
    return scaled_candidate(points, count, 1.0)


def face_centered_candidates(count: int) -> list[tuple[float, list[tuple[float, float, float]]]]:
    side = 1
    while ((side**3 + 1) // 2) < count:
        side += 1

    candidates: list[tuple[float, list[tuple[float, float, float]]]] = []
    for trial_side in range(max(1, side - 1), side + 2):
        for parity in (0, 1):
            points = [
                (x, y, z)
                for x in range(trial_side)
                for y in range(trial_side)
                for z in range(trial_side)
                if (x + y + z) % 2 == parity
            ]
            if len(points) >= count:
                candidates.append(scaled_candidate(points, count, math.sqrt(2.0)))
    return candidates


def body_centered_candidates(count: int) -> list[tuple[float, list[tuple[float, float, float]]]]:
    side = 1
    while side**3 + max(0, side - 1) ** 3 < count:
        side += 1

    candidates: list[tuple[float, list[tuple[float, float, float]]]] = []
    for trial_side in range(max(1, side - 1), side + 2):
        points = [
            (2 * x, 2 * y, 2 * z)
            for x in range(trial_side)
            for y in range(trial_side)
            for z in range(trial_side)
        ]
        points.extend(
            (2 * x + 1, 2 * y + 1, 2 * z + 1)
            for x in range(max(0, trial_side - 1))
            for y in range(max(0, trial_side - 1))
            for z in range(max(0, trial_side - 1))
        )
        if len(points) >= count:
            candidates.append(scaled_candidate(points, count, math.sqrt(3.0)))
    return candidates


def diagonal_pair() -> tuple[float, list[tuple[float, float, float]]]:
    radius = math.sqrt(3.0) / (2.0 * (1.0 + math.sqrt(3.0)))
    return radius, [
        (radius, radius, radius),
        (1.0 - radius, 1.0 - radius, 1.0 - radius),
    ]


def construct(count: int) -> list[tuple[float, float, float]]:
    candidates = [simple_cubic_candidate(count)]
    candidates.extend(face_centered_candidates(count))
    candidates.extend(body_centered_candidates(count))
    if count == 2:
        candidates.append(diagonal_pair())

    _, coordinates = max(candidates, key=lambda candidate: candidate[0])
    return coordinates


def main() -> int:
    tokens = sys.stdin.read().split()
    if not tokens:
        return 1
    count = int(tokens[0])
    if count <= 0:
        return 1
    for x, y, z in construct(count):
        print(f"{x:.12f} {y:.12f} {z:.12f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
