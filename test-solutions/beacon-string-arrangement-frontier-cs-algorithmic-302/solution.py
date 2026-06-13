from __future__ import annotations

import sys


MAX_MOTIF_LEN = 10


def block_string(counts: list[int], order: list[int]) -> str:
    return "".join(chr(ord("a") + idx) * counts[idx] for idx in order)


def suffix_penalty(tail: str, ch: str, motifs_by_len: list[dict[str, int]]) -> int:
    text = tail + ch
    limit = min(MAX_MOTIF_LEN, len(text))
    penalty = 0
    for length in range(2, limit + 1):
        penalty += motifs_by_len[length].get(text[-length:], 0)
    return penalty


def total_penalty(s: str, weights: list[list[int]], motifs_by_len: list[dict[str, int]]) -> int:
    if not s:
        return 0
    total = 0
    prev = ord(s[0]) - ord("a")
    tail = s[0]
    for ch in s[1:]:
        cur = ord(ch) - ord("a")
        total += weights[prev][cur]
        total += suffix_penalty(tail[-(MAX_MOTIF_LEN - 1):], ch, motifs_by_len)
        tail = (tail + ch)[-(MAX_MOTIF_LEN - 1):]
        prev = cur
    return total


def nearest_neighbor_order(k: int, counts: list[int], weights: list[list[int]]) -> list[int]:
    if k == 1:
        return [0]
    unused = set(range(k))
    start = min(unused, key=lambda i: (weights[i][i], -counts[i], i))
    order = [start]
    unused.remove(start)
    while unused:
        last = order[-1]
        nxt = min(unused, key=lambda i: (weights[last][i], weights[i][i], -counts[i], i))
        order.append(nxt)
        unused.remove(nxt)
    return order


def greedy_string(
    n: int,
    k: int,
    counts: list[int],
    weights: list[list[int]],
    motifs_by_len: list[dict[str, int]],
) -> str:
    remaining = counts[:]
    output: list[str] = []
    tail = ""
    prev = -1
    average_edge = max(1, sum(sum(row) for row in weights) // max(1, k * k))
    average_motif = max(
        0,
        sum(sum(bucket.values()) for bucket in motifs_by_len) // max(1, sum(len(bucket) for bucket in motifs_by_len)),
    )
    balance_weight = max(1, (average_edge + average_motif) // 4)

    for pos in range(n):
        slots_left = n - pos
        best_idx = -1
        best_key: tuple[float, int, int] | None = None
        for idx in range(k):
            if remaining[idx] <= 0:
                continue
            ch = chr(ord("a") + idx)
            immediate = 0 if prev < 0 else weights[prev][idx]
            immediate += suffix_penalty(tail, ch, motifs_by_len)
            pressure = balance_weight * remaining[idx] / slots_left
            key = (immediate - pressure, -remaining[idx], idx)
            if best_key is None or key < best_key:
                best_key = key
                best_idx = idx
        ch = chr(ord("a") + best_idx)
        output.append(ch)
        remaining[best_idx] -= 1
        prev = best_idx
        tail = (tail + ch)[-(MAX_MOTIF_LEN - 1):]
    return "".join(output)


def main() -> int:
    tokens = sys.stdin.read().split()
    if not tokens:
        return 0
    pos = 0
    n = int(tokens[pos])
    k = int(tokens[pos + 1])
    pos += 2
    counts = [int(tokens[pos + i]) for i in range(k)]
    pos += k
    weights = [[0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            weights[i][j] = int(tokens[pos])
            pos += 1
    m = int(tokens[pos])
    pos += 1

    motifs_by_len: list[dict[str, int]] = [dict() for _ in range(MAX_MOTIF_LEN + 1)]
    for _ in range(m):
        pattern = tokens[pos]
        weight = int(tokens[pos + 1])
        pos += 2
        if 2 <= len(pattern) <= MAX_MOTIF_LEN:
            motifs_by_len[len(pattern)][pattern] = motifs_by_len[len(pattern)].get(pattern, 0) + weight

    natural_order = list(range(k))
    reverse_order = list(reversed(natural_order))
    path_order = nearest_neighbor_order(k, counts, weights)
    candidates = [
        block_string(counts, natural_order),
        block_string(counts, reverse_order),
        block_string(counts, path_order),
        greedy_string(n, k, counts, weights, motifs_by_len),
    ]
    best = min(candidates, key=lambda candidate: total_penalty(candidate, weights, motifs_by_len))
    sys.stdout.write(best + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
