from __future__ import annotations

import random
import sys


def simulate(a: list[int], b: list[int], target: list[int], weeks: int) -> int:
    counts = [0] * len(target)
    cur = 0
    for _ in range(weeks):
        counts[cur] += 1
        cur = a[cur] if counts[cur] & 1 else b[cur]
    return sum(abs(counts[i] - target[i]) for i in range(len(target)))


def greedy_assignment(
    bundles: list[tuple[int, int, int]],
    required: list[int],
    order: list[int],
) -> tuple[list[int], list[int]]:
    n = len(required)
    assigned = [0] * n
    a = [0] * n
    b = [0] * n

    for bundle_idx in order:
        weight, slot, source = bundles[bundle_idx]
        best = max(range(n), key=lambda y: (required[y] - assigned[y], -y))
        assigned[best] += weight
        if slot == 0:
            a[source] = best
        else:
            b[source] = best

    return a, b


def solve() -> None:
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    weeks = int(tokens[1])
    target = [int(x) for x in tokens[2:2 + n]]

    required = target[:]
    required[0] = max(0, required[0] - 1)

    bundles: list[tuple[int, int, int]] = []
    for source, visits in enumerate(target):
        odd_weight = (visits + 1) // 2
        even_weight = visits // 2
        if odd_weight:
            bundles.append((odd_weight, 0, source))
        if even_weight:
            bundles.append((even_weight, 1, source))

    base_order = sorted(range(len(bundles)), key=lambda i: (-bundles[i][0], bundles[i][2], bundles[i][1]))
    candidate_orders = [base_order, list(reversed(base_order))]

    rng = random.Random(170)
    for _ in range(6):
        order = base_order[:]
        rng.shuffle(order)
        candidate_orders.append(order)

    best_error: int | None = None
    best_a: list[int] = [0] * n
    best_b: list[int] = [0] * n
    for order in candidate_orders:
        a, b = greedy_assignment(bundles, required, order)
        error = simulate(a, b, target, weeks)
        if best_error is None or error < best_error:
            best_error = error
            best_a = a
            best_b = b

    sys.stdout.write("\n".join(f"{best_a[i]} {best_b[i]}" for i in range(n)) + "\n")


if __name__ == "__main__":
    solve()
