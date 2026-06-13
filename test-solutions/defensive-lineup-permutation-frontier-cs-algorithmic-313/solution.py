from __future__ import annotations

from array import array
from collections import deque
import sys


class AhoCorasick:
    def __init__(self, patterns: list[str]) -> None:
        self.next: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.out: list[list[int]] = [[]]

        for pid, pattern in enumerate(patterns):
            node = 0
            for ch in pattern:
                nxt = self.next[node]
                if ch not in nxt:
                    nxt[ch] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.out.append([])
                node = nxt[ch]
            self.out[node].append(pid)

        queue: deque[int] = deque(self.next[0].values())
        while queue:
            node = queue.popleft()
            for ch, child in self.next[node].items():
                fail = self.fail[node]
                while fail and ch not in self.next[fail]:
                    fail = self.fail[fail]
                self.fail[child] = self.next[fail].get(ch, 0)
                self.out[child].extend(self.out[self.fail[child]])
                queue.append(child)

    def scan_scalar(self, text: str, values: list[int]) -> int:
        node = 0
        total = 0
        for ch in text:
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            for pid in self.out[node]:
                total += values[pid]
        return total

    def scan_edge_cost(self, text: str, edge_pos: int, weights: list[array[int]]) -> int:
        node = 0
        total = 0
        for ch in text:
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            for pid in self.out[node]:
                total += weights[pid][edge_pos]
        return total


def main() -> int:
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return 0

    n = int(tokens[0])
    q = int(tokens[1])
    names = [""] + [tokens[2 + i].decode("ascii") for i in range(n)]
    if n == 1:
        sys.stdout.write("1\n")
        return 0

    pattern_to_id: dict[str, int] = {}
    patterns: list[str] = []
    pattern_diffs: list[array[int]] = []

    def pattern_id(pattern: str) -> int:
        existing = pattern_to_id.get(pattern)
        if existing is not None:
            return existing
        pid = len(patterns)
        pattern_to_id[pattern] = pid
        patterns.append(pattern)
        pattern_diffs.append(array("q", [0]) * (n + 1))
        return pid

    edge_diff = array("q", [0]) * (n + 1)
    pos = 2 + n
    for _ in range(q):
        left = int(tokens[pos])
        right = int(tokens[pos + 1])
        target = int(tokens[pos + 2])
        pos += 3
        pid = pattern_id(names[target])
        pattern_diffs[pid][left] += 1
        pattern_diffs[pid][right] -= 1
        edge_diff[left] += 1
        edge_diff[right] -= 1

    pattern_totals = [0] * len(patterns)
    for pid, diff in enumerate(pattern_diffs):
        running = 0
        total = 0
        for edge_pos in range(1, n):
            running += diff[edge_pos]
            diff[edge_pos] = running
            total += running
        pattern_totals[pid] = total

    edge_cover = [0] * n
    running = 0
    for edge_pos in range(1, n):
        running += edge_diff[edge_pos]
        edge_cover[edge_pos] = running

    seat_exposure = [0] * (n + 1)
    for seat in range(1, n + 1):
        left = edge_cover[seat - 1] if seat > 1 else 0
        right = edge_cover[seat] if seat < n else 0
        seat_exposure[seat] = left + right

    matcher = AhoCorasick(patterns)

    intrinsic = [0] * (n + 1)
    for idx in range(1, n + 1):
        intrinsic[idx] = matcher.scan_scalar(names[idx], pattern_totals)

    def exact_cost(perm: list[int]) -> int:
        total = 0
        for edge_pos in range(1, n):
            merged = names[perm[edge_pos - 1]] + names[perm[edge_pos]]
            total += matcher.scan_edge_cost(merged, edge_pos, pattern_diffs)
        return total

    candidates: list[list[int]] = []
    identity = list(range(1, n + 1))
    candidates.append(identity)
    candidates.append(list(reversed(identity)))
    candidates.append(sorted(identity, key=lambda idx: (names[idx], idx)))
    candidates.append(sorted(identity, key=lambda idx: (names[idx][0], len(names[idx]), names[idx], idx)))

    burdened_friends = sorted(identity, key=lambda idx: (-intrinsic[idx], names[idx], idx))
    quiet_positions = sorted(range(1, n + 1), key=lambda seat: (seat_exposure[seat], seat))
    exposure_perm = [0] * n
    for seat, friend in zip(quiet_positions, burdened_friends, strict=True):
        exposure_perm[seat - 1] = friend
    candidates.append(exposure_perm)

    best_perm = identity
    best_cost = exact_cost(identity)
    seen: set[tuple[int, ...]] = {tuple(identity)}
    for perm in candidates[1:]:
        key = tuple(perm)
        if key in seen:
            continue
        seen.add(key)
        cost = exact_cost(perm)
        if cost < best_cost:
            best_cost = cost
            best_perm = perm

    sys.stdout.write(" ".join(map(str, best_perm)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
