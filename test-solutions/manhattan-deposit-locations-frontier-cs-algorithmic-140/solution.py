from __future__ import annotations

import sys

PROBE = 100_000_000


def ask_one(x: int, y: int) -> int:
    print(f"? 1 {x} {y}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed while answering a wave")
    return int(line.strip().split()[0])


def answer(points: list[tuple[int, int]]) -> None:
    flat = " ".join(f"{x} {y}" for x, y in points)
    print(f"! {flat}", flush=True)


def main() -> int:
    first = sys.stdin.readline()
    if not first:
        return 0
    _bound, deposits, waves = map(int, first.split())

    if deposits == 1:
        distance_to_origin = ask_one(0, 0)
        if distance_to_origin == 0:
            answer([(0, 0)])
            return 0
        if waves >= 5:
            dist_pos_x = ask_one(PROBE, 0)
            dist_neg_x = ask_one(-PROBE, 0)
            dist_pos_y = ask_one(0, PROBE)
            dist_neg_y = ask_one(0, -PROBE)
            x = (dist_neg_x - dist_pos_x) // 2
            y = (dist_neg_y - dist_pos_y) // 2
            answer([(x, y)])
            return 0
        answer([(0, 0)])
        return 0

    answer([(0, 0) for _ in range(deposits)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
