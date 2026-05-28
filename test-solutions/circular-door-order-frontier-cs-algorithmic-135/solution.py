from __future__ import annotations

import itertools
import sys


def query(x: int, y: int, z: int) -> set[tuple[int, int]]:
    print(f"? {x} {y} {z}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise SystemExit(0)
    count = int(line.strip())
    pairs: set[tuple[int, int]] = set()
    for _ in range(count):
        a, b = map(int, sys.stdin.readline().split())
        if a > b:
            a, b = b, a
        pairs.add((a, b))
    return pairs


def closest_pairs(order: tuple[int, ...], triple: tuple[int, int, int]) -> set[tuple[int, int]]:
    n = len(order)
    pos = {value: index for index, value in enumerate(order)}
    distances: list[tuple[int, tuple[int, int]]] = []
    for a, b in itertools.combinations(triple, 2):
        diff = abs(pos[a] - pos[b])
        dist = min(diff, n - diff)
        if a > b:
            a, b = b, a
        distances.append((dist, (a, b)))
    best = min(dist for dist, _ in distances)
    return {pair for dist, pair in distances if dist == best}


def solve_small(n: int) -> list[int] | None:
    observations: dict[tuple[int, int, int], set[tuple[int, int]]] = {}
    for triple in itertools.combinations(range(n), 3):
        observations[triple] = query(*triple)

    for tail in itertools.permutations(range(1, n)):
        order = (0, *tail)
        if order[1] > order[-1]:
            continue
        if all(closest_pairs(order, triple) == result for triple, result in observations.items()):
            return list(order)
    return None


def main() -> int:
    line = sys.stdin.readline()
    if line == "":
        return 0
    _, n = map(int, line.split())
    if n <= 2:
        print("! " + " ".join(str(i) for i in range(n)), flush=True)
        return 0
    if n <= 9:
        order = solve_small(n)
        if order is not None:
            print("! " + " ".join(map(str, order)), flush=True)
            return 0

    print("! " + " ".join(str(i) for i in range(n)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
