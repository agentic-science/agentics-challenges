from __future__ import annotations

import sys
from collections import deque
from functools import lru_cache

A, B, P, Q, R, C = range(6)


def build_states() -> tuple[list[tuple[int, ...]], list[tuple[int, int]], list[tuple]]:
    states: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for t1 in range(3):
        for t2 in range(3):
            for t3 in range(3):
                order = [A, B, C]
                order.insert(t1, P)
                order.insert(t2, Q)
                order.insert(t3, R)
                state = tuple(label for label in order if label != C)
                if state not in seen:
                    seen.add(state)
                    states.append(state)

    pairs = [(u, v) for u in range(5) for v in range(u + 1, 5) if (u, v) != (A, B)]
    outcomes: list[list[bool]] = []
    for state in states:
        position = {label: index for index, label in enumerate(state)}
        outcomes.append([position[u] < position[v] for u, v in pairs])

    nodes: list[tuple] = []

    @lru_cache(maxsize=None)
    def build(mask: int, depth: int) -> int:
        if mask & (mask - 1) == 0:
            state_index = (mask & -mask).bit_length() - 1
            nodes.append(("leaf", state_index))
            return len(nodes) - 1
        if depth == 0:
            return -1

        best_pair: int | None = None
        best_score = -1
        for pair_index in range(len(pairs)):
            left_mask = 0
            for state_index in range(len(states)):
                if mask & (1 << state_index) and outcomes[state_index][pair_index]:
                    left_mask |= 1 << state_index
            right_mask = mask & ~left_mask
            if not left_mask or not right_mask:
                continue
            score = min(left_mask.bit_count(), right_mask.bit_count())
            if score > best_score:
                best_score = score
                best_pair = pair_index

        pair_order = []
        if best_pair is not None:
            pair_order.append(best_pair)
        pair_order.extend(pair_index for pair_index in range(len(pairs)) if pair_index != best_pair)

        for pair_index in pair_order:
            left_mask = 0
            for state_index in range(len(states)):
                if mask & (1 << state_index) and outcomes[state_index][pair_index]:
                    left_mask |= 1 << state_index
            right_mask = mask & ~left_mask
            if not left_mask or not right_mask:
                continue
            left = build(left_mask, depth - 1)
            right = build(right_mask, depth - 1)
            if left == -1 or right == -1:
                continue
            nodes.append(("node", pair_index, left, right))
            return len(nodes) - 1

        return -1

    full_mask = (1 << len(states)) - 1
    root = build(full_mask, 5)
    if root == -1:
        raise RuntimeError("failed to build decision tree")
    nodes.append(("root", root))
    return states, pairs, nodes


STATES, PAIRS, NODES_WITH_ROOT = build_states()
ROOT = NODES_WITH_ROOT[-1][1]
NODES = NODES_WITH_ROOT[:-1]


def ask(i: int, j: int) -> bool:
    print(f"? {i} {j}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactive evaluator closed before answering")
    return line.strip() == "<"


def sort3(i: int, j: int, k: int) -> list[int]:
    a, b, c = i, j, k
    if ask(b, a):
        a, b = b, a
    if ask(c, b):
        b, c = c, b
    if ask(b, a):
        a, b = b, a
    return [a, b, c]


def solve(n: int) -> list[int]:
    if n == 1:
        return [0, 1]
    if n == 2:
        order = [1, 2] if ask(1, 2) else [2, 1]
        answer = [0] * (n + 1)
        for rank, index in enumerate(order, start=1):
            answer[index] = rank
        return answer

    top = sort3(n - 2, n - 1, n)
    tail: deque[int] = deque()

    def insert_one(index: int) -> None:
        nonlocal top
        a, b, c = top
        if ask(b, index):
            tail.appendleft(c)
            top = [a, b, index]
            return
        if ask(index, a):
            tail.appendleft(c)
            top = [index, a, b]
        else:
            tail.appendleft(c)
            top = [a, index, b]

    current = n - 3
    while current >= 3:
        p = current
        q = current - 1
        r = current - 2
        old_third = top[2]
        index_by_label = {A: top[0], B: top[1], P: p, Q: q, R: r}

        node_index = ROOT
        while NODES[node_index][0] != "leaf":
            _, pair_index, left, right = NODES[node_index]
            u, v = PAIRS[pair_index]
            node_index = left if ask(index_by_label[u], index_by_label[v]) else right

        state = STATES[NODES[node_index][1]]
        ordered = [index_by_label[label] for label in state]
        tail.appendleft(old_third)
        tail.appendleft(ordered[4])
        tail.appendleft(ordered[3])
        top = ordered[:3]
        current -= 3

    for index in range(current, 0, -1):
        insert_one(index)

    order = top + list(tail)
    answer = [0] * (n + 1)
    for rank, index in enumerate(order, start=1):
        answer[index] = rank
    return answer


def main() -> int:
    line = sys.stdin.readline()
    if line == "":
        return 0
    n = int(line.strip())
    answer = solve(n)
    print("! " + " ".join(str(answer[index]) for index in range(1, n + 1)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
