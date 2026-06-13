from __future__ import annotations

import bisect
import sys


EXACT_N_LIMIT = 34
BEAM_WIDTH = 512


def enumerate_half(values: list[int], offset: int) -> list[tuple[int, int]]:
    states: list[tuple[int, int]] = [(0, 0)]
    for i, value in enumerate(values):
        bit = 1 << (offset + i)
        states += [(total + value, mask | bit) for total, mask in states]
    states.sort(key=lambda item: item[0])
    return states


def exact_nearest(values: list[int], target: int) -> int:
    mid = len(values) // 2
    left = enumerate_half(values[:mid], 0)
    right = enumerate_half(values[mid:], mid)
    right_sums = [total for total, _ in right]

    best_sum = 0
    best_mask = 0
    best_diff = abs(target)

    def consider(total: int, mask: int) -> None:
        nonlocal best_sum, best_mask, best_diff
        diff = abs(target - total)
        if diff < best_diff or (diff == best_diff and total <= target < best_sum):
            best_sum = total
            best_mask = mask
            best_diff = diff

    for left_sum, left_mask in left:
        pos = bisect.bisect_left(right_sums, target - left_sum)
        for j in (pos - 1, pos, pos + 1):
            if 0 <= j < len(right):
                right_sum, right_mask = right[j]
                consider(left_sum + right_sum, left_mask | right_mask)
    return best_mask


def greedy_masks(values: list[int], target: int) -> list[int]:
    order_desc = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    order_asc = list(reversed(order_desc))
    masks: list[int] = []

    for order, allow_overshoot in ((order_desc, False), (order_asc, False), (order_desc, True)):
        total = 0
        mask = 0
        for idx in order:
            candidate = total + values[idx]
            if allow_overshoot:
                if abs(target - candidate) < abs(target - total):
                    total = candidate
                    mask |= 1 << idx
            elif candidate <= target:
                total = candidate
                mask |= 1 << idx
        masks.append(mask)
    return masks


def beam_search(values: list[int], target: int) -> int:
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    states: list[tuple[int, int]] = [(0, 0)]
    best_total = 0
    best_mask = 0
    best_diff = abs(target)

    def consider(total: int, mask: int) -> None:
        nonlocal best_total, best_mask, best_diff
        diff = abs(target - total)
        if diff < best_diff or (diff == best_diff and total <= target < best_total):
            best_total = total
            best_mask = mask
            best_diff = diff

    for idx in order:
        value = values[idx]
        bit = 1 << idx
        expanded = states + [(total + value, mask | bit) for total, mask in states]
        expanded.sort(key=lambda item: abs(target - item[0]))

        next_states: list[tuple[int, int]] = []
        seen: set[int] = set()
        for total, mask in expanded:
            if total in seen:
                continue
            seen.add(total)
            next_states.append((total, mask))
            consider(total, mask)
            if len(next_states) >= BEAM_WIDTH:
                break
        states = next_states
    return best_mask


def main() -> int:
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return 0
    n = int(tokens[0])
    target = int(tokens[1])
    values = [int(token) for token in tokens[2:2 + n]]

    candidate_masks = [0]
    total_sum = sum(values)
    if total_sum:
        candidate_masks.append((1 << n) - 1)
    for idx, value in enumerate(values):
        if value:
            candidate_masks.append(1 << idx)

    if n <= EXACT_N_LIMIT:
        candidate_masks.append(exact_nearest(values, target))
    else:
        candidate_masks.extend(greedy_masks(values, target))
        candidate_masks.append(beam_search(values, target))

    best_mask = 0
    best_diff = abs(target)
    for mask in candidate_masks:
        total = 0
        bits = mask
        while bits:
            low = bits & -bits
            total += values[low.bit_length() - 1]
            bits -= low
        diff = abs(target - total)
        if diff < best_diff:
            best_diff = diff
            best_mask = mask

    sys.stdout.write(" ".join("1" if (best_mask >> i) & 1 else "0" for i in range(n)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
