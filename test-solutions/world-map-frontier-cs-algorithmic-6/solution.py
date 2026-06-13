from __future__ import annotations

from collections import deque
import sys


MAX_K = 240


def connected_component(root: int, adjacency: list[set[int]], seen: set[int]) -> list[int]:
    queue: deque[int] = deque([root])
    seen.add(root)
    component: list[int] = []
    while queue:
        vertex = queue.popleft()
        component.append(vertex)
        for neighbor in sorted(adjacency[vertex]):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return component


def build_tree(root: int, component: set[int], adjacency: list[set[int]]) -> dict[int, list[int]]:
    tree = {vertex: [] for vertex in component}
    parent = {root}
    queue: deque[int] = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbor in sorted(adjacency[vertex]):
            if neighbor not in component or neighbor in parent:
                continue
            parent.add(neighbor)
            tree[vertex].append(neighbor)
            queue.append(neighbor)
    return tree


def construct_grid(n: int, edges: set[tuple[int, int]]) -> list[list[int]]:
    if not edges:
        return [[1]]

    adjacency = [set() for _ in range(n + 1)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    seen: set[int] = set()
    components: list[list[int]] = []
    for vertex in range(1, n + 1):
        if adjacency[vertex] and vertex not in seen:
            components.append(connected_component(vertex, adjacency, seen))

    # A grid's visible color-adjacency graph is connected, so multiple edge-bearing
    # components cannot be represented exactly. Use one component to keep output bounded.
    component = max(components, key=len)
    component_set = set(component)
    root = min(component)
    tree = build_tree(root, component_set, adjacency)
    min_width = max(1, max(2 * len(adjacency[vertex]) + 1 for vertex in component))

    rows: list[tuple[int, list[int] | None]] = []

    def add_constant(vertex: int) -> None:
        if rows and rows[-1][1] is None and rows[-1][0] == vertex:
            return
        rows.append((vertex, None))

    def add_gadget(vertex: int) -> None:
        row = [vertex]
        for neighbor in sorted(adjacency[vertex]):
            row.extend([neighbor, vertex])
        rows.append((vertex, row))

    def dfs(vertex: int) -> None:
        add_gadget(vertex)
        add_constant(vertex)
        for child in tree[vertex]:
            add_constant(child)
            dfs(child)
            add_constant(vertex)

    add_constant(root)
    dfs(root)

    k = max(min_width, len(rows), 1)
    if k > MAX_K:
        return [[1]]

    while len(rows) < k:
        rows.append((root, None))

    grid: list[list[int]] = []
    for base, partial in rows:
        if partial is None:
            grid.append([base] * k)
            continue
        grid.append(partial + [base] * (k - len(partial)))
    return grid


def main() -> int:
    tokens = [int(token) for token in sys.stdin.read().split()]
    if len(tokens) < 2:
        return 1
    n, m = tokens[0], tokens[1]
    edges = {tuple(sorted((tokens[index], tokens[index + 1]))) for index in range(2, 2 + 2 * m, 2)}
    grid = construct_grid(n, edges)
    k = len(grid)
    print(k)
    print(" ".join([str(k)] * k))
    for row in grid:
        print(" ".join(str(value) for value in row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
