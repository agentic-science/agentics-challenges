from __future__ import annotations

import sys
from collections import deque


def read_int_line() -> int | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        line = line.strip()
        if line:
            return int(line)


def query(node: int) -> int:
    print(f"? {node}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    return int(line.strip())


def answer(node: int) -> None:
    print(f"! {node}", flush=True)


def build_rooted_tree(n: int, graph: list[list[int]]) -> tuple[list[int], list[int], list[int], list[int], list[int]]:
    parent = [1] * (n + 1)
    depth = [0] * (n + 1)
    order: list[int] = []
    stack = [(1, 0, 0)]
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    timer = 0

    while stack:
        node, prev, state = stack.pop()
        if state == 0:
            parent[node] = 1 if prev == 0 else prev
            timer += 1
            tin[node] = timer
            order.append(node)
            stack.append((node, prev, 1))
            for nxt in reversed(graph[node]):
                if nxt == prev:
                    continue
                depth[nxt] = depth[node] + 1
                stack.append((nxt, node, 0))
        else:
            tout[node] = timer

    return parent, depth, tin, tout, order


def solve_case(n: int) -> None:
    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        line = sys.stdin.readline()
        if not line:
            raise EOFError("missing tree edge")
        u, v = map(int, line.split())
        graph[u].append(v)
        graph[v].append(u)

    parent, _depth, tin, tout, order = build_rooted_tree(n, graph)
    alive = [False] + [True] * n
    cur_pos = list(range(n + 1))
    query_count = 0

    while True:
        candidates = [node for node in range(1, n + 1) if alive[node]]
        if not candidates:
            answer(1)
            return

        weights = [0] * (n + 1)
        distinct = 0
        last_pos = 1
        for node in candidates:
            pos = cur_pos[node]
            if weights[pos] == 0:
                distinct += 1
                last_pos = pos
            weights[pos] += 1

        if distinct == 1 or query_count >= 160:
            answer(last_pos)
            return

        subtree = weights[:]
        for node in reversed(order):
            if node != 1:
                subtree[parent[node]] += subtree[node]

        total = len(candidates)
        best_node = 1
        best_value = total + 1
        for node in range(1, n + 1):
            inside = subtree[node]
            if inside == 0 or inside == total:
                continue
            value = max(inside, total - inside)
            if value < best_value:
                best_value = value
                best_node = node

        if best_value == total + 1:
            answer(last_pos)
            return

        reply = query(best_node)
        query_count += 1
        for node in candidates:
            pos = cur_pos[node]
            inside = tin[best_node] <= tin[pos] <= tout[best_node]
            if reply == 1:
                if not inside:
                    alive[node] = False
            elif inside:
                alive[node] = False
            elif pos != 1:
                cur_pos[node] = parent[pos]


def main() -> int:
    while True:
        test_count = read_int_line()
        if test_count is None or test_count <= 0:
            return 0
        for _ in range(test_count):
            n = read_int_line()
            if n is None:
                return 0
            solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
