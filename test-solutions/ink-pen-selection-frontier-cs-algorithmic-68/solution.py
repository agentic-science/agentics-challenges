from __future__ import annotations

import sys

MAX_TRIES_PER_CASE = 4096
MAX_PROBED_INDICES = 2048


def try_pen(index: int) -> int:
    print(f"0 {index}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactive evaluator closed before replying")
    return int(line.strip())


def candidate_indices(n: int) -> list[int]:
    if n <= MAX_PROBED_INDICES:
        return list(range(n))

    seen: set[int] = set()
    result: list[int] = []

    for index in (0, 1, n - 2, n - 1):
        if 0 <= index < n and index not in seen:
            seen.add(index)
            result.append(index)

    slots = MAX_PROBED_INDICES - len(result)
    for slot in range(slots):
        index = (slot * n) // max(1, slots)
        if index not in seen:
            seen.add(index)
            result.append(index)

    return result


def solve_case(n: int) -> None:
    threshold = min(3, max(1, n // 4))
    scores: dict[int, int] = {}
    tries = 0
    candidates = candidate_indices(n)

    for index in candidates:
        if tries >= MAX_TRIES_PER_CASE:
            break
        scores[index] = 0
        for _ in range(threshold):
            if tries >= MAX_TRIES_PER_CASE:
                break
            tries += 1
            if try_pen(index) == 1:
                scores[index] += 1
            else:
                break

    chosen = sorted(candidates, key=lambda i: (scores.get(i, 0), i), reverse=True)[:2]
    if len(chosen) < 2:
        chosen = []
        for index in range(n):
            if index not in chosen:
                chosen.append(index)
            if len(chosen) == 2:
                break
    print(f"1 {chosen[0]} {chosen[1]}", flush=True)


def main() -> None:
    while True:
        first = sys.stdin.readline()
        if first == "":
            return
        first = first.strip()
        if not first:
            continue
        t = int(first)
        for _ in range(t):
            line = sys.stdin.readline()
            if line == "":
                return
            solve_case(int(line.strip()))


if __name__ == "__main__":
    main()
