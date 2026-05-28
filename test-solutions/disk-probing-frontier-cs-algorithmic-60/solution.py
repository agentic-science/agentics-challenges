from __future__ import annotations

import sys

MAX_COORD = 100000
STEP = 128
EPS = 1e-7


def probe(x1: int, y1: int, x2: int, y2: int) -> float:
    print(f"query {x1} {y1} {x2} {y2}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactive evaluator closed before replying")
    return float(line.strip())


def vertical_length(x: int) -> float:
    return probe(x, 0, x, MAX_COORD)


def has_vertical_hit(x: int) -> bool:
    return vertical_length(x) > EPS


def main() -> None:
    hit: int | None = None
    for x in range(0, MAX_COORD + 1, STEP):
        if has_vertical_hit(x):
            hit = x
            break
    if hit is None:
        for x in range(MAX_COORD, -1, -STEP):
            if has_vertical_hit(x):
                hit = x
                break
    if hit is None:
        return

    lo, hi = 0, hit
    while lo < hi:
        mid = (lo + hi) // 2
        if has_vertical_hit(mid):
            hi = mid
        else:
            lo = mid + 1
    left = lo

    lo, hi = hit, MAX_COORD
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if has_vertical_hit(mid):
            lo = mid
        else:
            hi = mid - 1
    right = lo

    cx = (left + right) // 2
    r = round(vertical_length(cx) / 2.0)

    lo, hi = 1, MAX_COORD
    while lo < hi:
        mid = (lo + hi) // 2
        if probe(cx, 0, cx, mid) > EPS:
            hi = mid
        else:
            lo = mid + 1
    cy = lo + r - 1

    print(f"answer {cx} {cy} {r}", flush=True)


if __name__ == "__main__":
    main()
