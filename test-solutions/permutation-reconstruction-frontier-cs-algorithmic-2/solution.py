from __future__ import annotations

import random
import sys


def ask(values: list[int]) -> int:
    print("0 " + " ".join(str(value) for value in values), flush=True)
    reply = sys.stdin.readline()
    if reply == "":
        raise RuntimeError("interactive evaluator closed stdin")
    return int(reply.strip())


def locate_with_anchor(
    *,
    n: int,
    target_value: int,
    anchor_value: int,
    candidates: list[int],
) -> int:
    remaining = candidates[:]
    while len(remaining) > 1:
        midpoint = len(remaining) // 2
        left = remaining[:midpoint]
        left_set = set(left)
        probe = [
            target_value if position in left_set else anchor_value for position in range(n)
        ]
        matches = ask(probe)
        remaining = left if matches > 1 else remaining[midpoint:]
    return remaining[0]


def split_anchor_pair(n: int) -> tuple[list[int], list[int]]:
    positions = list(range(n))
    rng = random.Random(2)
    if n == 2:
        subsets = [[0]]
    else:
        subsets = []

    for _ in range(64):
        subset = [position for position in positions if rng.getrandbits(1) == 1]
        if subset and len(subset) < n:
            subsets.append(subset)

    for subset in subsets:
        subset_set = set(subset)
        probe = [1 if position in subset_set else 2 for position in positions]
        matches = ask(probe)
        complement = [position for position in positions if position not in subset_set]
        if matches == 2:
            return subset, complement
        if matches == 0:
            return complement, subset

    raise RuntimeError("failed to separate anchor values")


def main() -> None:
    first = sys.stdin.readline()
    if first == "":
        return
    n = int(first.strip())
    if n <= 0:
        return
    if n == 1:
        print("1 1", flush=True)
        return

    one_candidates, two_candidates = split_anchor_pair(n)
    pos_one = locate_with_anchor(
        n=n,
        target_value=1,
        anchor_value=2,
        candidates=one_candidates,
    )
    pos_two = locate_with_anchor(
        n=n,
        target_value=2,
        anchor_value=1,
        candidates=two_candidates,
    )

    permutation = [0] * n
    permutation[pos_one] = 1
    permutation[pos_two] = 2
    remaining_positions = [
        position for position in range(n) if position not in {pos_one, pos_two}
    ]

    for value in range(3, n + 1):
        position = locate_with_anchor(
            n=n,
            target_value=value,
            anchor_value=1,
            candidates=remaining_positions,
        )
        permutation[position] = value
        remaining_positions.remove(position)

    print("1 " + " ".join(str(value) for value in permutation), flush=True)


if __name__ == "__main__":
    main()
