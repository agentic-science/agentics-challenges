from __future__ import annotations

import math
import sys
from collections import deque

State = tuple[int, int, int]


def update_with_same_count(states: tuple[State, ...], l: int, r: int, out: int) -> tuple[tuple[State, ...], int]:
    next_states: list[State] = []
    same_count = 0
    for ident, old0, old1 in states:
        truthful_count = r - l if l <= ident <= r else r - l + 1
        op = 1 if truthful_count == out else 0
        if old0 == op and old1 == op:
            continue
        state = (ident, old1, op)
        next_states.append(state)
        if state[1] == state[2]:
            same_count += 1
    return tuple(next_states), same_count


def update(states: tuple[State, ...], l: int, r: int, out: int) -> tuple[State, ...]:
    next_states, _ = update_with_same_count(states, l, r, out)
    return next_states


def source_step(states: tuple[State, ...], l: int, r: int) -> tuple[int, tuple[State, ...]]:
    false_states, false_same = update_with_same_count(states, l, r, r - l)
    true_states, true_same = update_with_same_count(states, l, r, r - l + 1)
    if len(false_states) > len(true_states):
        return r - l, false_states
    if len(true_states) > len(false_states):
        return r - l + 1, true_states
    if false_same < true_same:
        return r - l, false_states
    return r - l + 1, true_states


def distinct_ids(states: tuple[State, ...]) -> set[int]:
    return {ident for ident, _, _ in states}


def find_small_query(states: tuple[State, ...], n: int) -> tuple[int, int] | None:
    queue = deque([states])
    seen = {states}
    first_move: dict[tuple[State, ...], tuple[int, int]] = {}
    intervals = [(l, r) for l in range(1, n + 1) for r in range(l, n + 1)]
    while queue and len(seen) <= 20000:
        current = queue.popleft()
        if len(distinct_ids(current)) <= 2:
            return first_move.get(current)
        for l, r in intervals:
            _, next_states = source_step(current, l, r)
            if next_states in seen:
                continue
            seen.add(next_states)
            first_move[next_states] = first_move.get(current, (l, r))
            queue.append(next_states)
    return None


def choose_query(states: tuple[State, ...], n: int) -> tuple[int, int]:
    if n <= 12:
        small_query = find_small_query(states, n)
        if small_query is not None:
            return small_query

    ids = sorted(distinct_ids(states))
    candidates: set[tuple[int, int]] = set()
    if n <= 80:
        for l in range(1, n + 1):
            for r in range(l, n + 1):
                candidates.add((l, r))
    else:
        points = sorted(set([1, n] + ids[::max(1, len(ids) // 20)]))
        for i, l in enumerate(points):
            for r in points[i:]:
                candidates.add((l, r))
        for q in range(1, 10):
            cut = ids[min(len(ids) - 1, q * len(ids) // 10)]
            candidates.add((1, cut))
            candidates.add((cut, n))

    best = (10**18, 10**18, 1, n)
    current = len(ids)
    for l, r in candidates:
        false_states = update(states, l, r, r - l)
        true_states = update(states, l, r, r - l + 1)
        false_ids = len(distinct_ids(false_states))
        true_ids = len(distinct_ids(true_states))
        worst = max(false_ids, true_ids)
        total = false_ids + true_ids
        if worst >= current and current > 2:
            continue
        key = (worst, total, l, r)
        if key < best:
            best = key
    return best[2], best[3]


def ask(l: int, r: int) -> int:
    print(f"? {l} {r}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    return int(line.strip())


def guess(a: int) -> int:
    print(f"! {a}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    return int(line.strip())


def solve_case(n: int) -> None:
    states: tuple[State, ...] = tuple((ident, a, b) for ident in range(1, n + 1) for a in (0, 1) for b in (0, 1))
    limit = max(1, 2 * math.ceil(math.log(max(n, 2), 1.116)))
    queries = 0
    while queries < limit and len(distinct_ids(states)) > 2:
        l, r = choose_query(states, n)
        out = ask(l, r)
        states = update(states, l, r, out)
        queries += 1
        if not states:
            break
    ids = sorted(distinct_ids(states)) or [1]
    for candidate in ids[:2]:
        if guess(candidate) == 1:
            print("#", flush=True)
            return
        states = tuple(state for state in states if state[0] != candidate)
    remaining = sorted(distinct_ids(states))
    if remaining:
        # The source allows only two guesses, so this branch is a last-resort honest fallback.
        pass
    print("#", flush=True)


def main() -> int:
    first = sys.stdin.readline()
    if not first:
        return 0
    t = int(first.strip())
    for _ in range(t):
        line = sys.stdin.readline()
        if not line:
            return 0
        solve_case(int(line.strip()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
