from __future__ import annotations

import sys


def read_int() -> int | None:
    line = sys.stdin.readline()
    if not line:
        return None
    try:
        return int(line.strip())
    except ValueError:
        return None


def query(start: int, steps: int, subset: list[int]) -> int:
    print(
        f"? {start} {steps} {len(subset)} " + " ".join(map(str, subset)),
        flush=True,
    )
    reply = read_int()
    if reply is None or reply == -1:
        raise SystemExit(0)
    return reply


def discover_successor(room: int, n: int) -> int:
    candidates = list(range(1, n + 1))
    while len(candidates) > 1:
        mid = len(candidates) // 2
        left = candidates[:mid]
        if query(room, 1, left):
            candidates = left
        else:
            candidates = candidates[mid:]
    return candidates[0]


def solve_case(n: int) -> None:
    path: list[int] = []
    seen_at = [None] * (n + 1)
    current = 1
    while seen_at[current] is None:
        seen_at[current] = len(path)
        path.append(current)
        current = discover_successor(current, n)

    cycle = set(path[seen_at[current] :])
    known_answer = set(path)

    if len(cycle) <= n - len(cycle):
        probe_set = sorted(cycle)
        include_when = 1
    else:
        probe_set = [room for room in range(1, n + 1) if room not in cycle]
        include_when = 0

    answer = sorted(known_answer)
    for room in range(1, n + 1):
        if room in known_answer:
            continue
        if query(room, n, probe_set) == include_when:
            answer.append(room)

    answer.sort()
    print(f"! {len(answer)} " + " ".join(map(str, answer)), flush=True)


def main() -> int:
    while True:
        n = read_int()
        if n is None:
            return 0
        solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
