from __future__ import annotations

import sys


class Oracle:
    def __init__(self) -> None:
        self.cache: dict[tuple[int, ...], int] = {}

    def query(self, vertices: list[int]) -> int:
        if len(vertices) <= 1:
            return 0
        key = tuple(sorted(vertices))
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        print(f"? {len(key)}")
        print(" ".join(map(str, key)), flush=True)
        line = sys.stdin.readline()
        if not line:
            raise EOFError("interactive evaluator closed before answering")
        answer = int(line.strip())
        if answer < 0:
            raise RuntimeError("query rejected by evaluator")
        self.cache[key] = answer
        return answer


def find_next_layer(
    oracle: Oracle,
    current_layer: list[int],
    current_edges: int,
    candidates: list[int],
    crossing_edges: int,
    out: list[int],
) -> None:
    if crossing_edges == 0:
        return
    if len(candidates) == 1:
        out.append(candidates[0])
        return

    mid = len(candidates) // 2
    left = candidates[:mid]
    right = candidates[mid:]
    left_edges = oracle.query(left)
    left_crossing = oracle.query(current_layer + left) - current_edges - left_edges
    find_next_layer(oracle, current_layer, current_edges, left, left_crossing, out)
    find_next_layer(oracle, current_layer, current_edges, right, crossing_edges - left_crossing, out)


def find_vertex_with_neighbor(oracle: Oracle, left: list[int], right: list[int]) -> int:
    candidates = left
    while len(candidates) > 1:
        mid = len(candidates) // 2
        head = candidates[:mid]
        tail = candidates[mid:]
        if oracle.query(head + right) > 0:
            candidates = head
        else:
            candidates = tail
    return candidates[0]


def find_neighbor_in_set(oracle: Oracle, vertex: int, vertices: list[int]) -> int:
    candidates = vertices
    while len(candidates) > 1:
        mid = len(candidates) // 2
        left = candidates[:mid]
        right = candidates[mid:]
        if oracle.query([vertex] + left) - oracle.query(left) > 0:
            candidates = left
        else:
            candidates = right
    return candidates[0]


def find_edge_in_set(oracle: Oracle, vertices: list[int]) -> tuple[int, int]:
    if len(vertices) == 2:
        return vertices[0], vertices[1]

    mid = len(vertices) // 2
    left = vertices[:mid]
    right = vertices[mid:]

    if oracle.query(left) > 0:
        return find_edge_in_set(oracle, left)
    if oracle.query(right) > 0:
        return find_edge_in_set(oracle, right)

    u = find_vertex_with_neighbor(oracle, left, right)
    v = find_neighbor_in_set(oracle, u, right)
    return u, v


def find_parent(oracle: Oracle, vertex: int, previous_layer: list[int]) -> int:
    return find_neighbor_in_set(oracle, vertex, previous_layer)


def path_to_root(oracle: Oracle, vertex: int, layer_index: int, layers: list[list[int]]) -> list[int]:
    path = [vertex]
    current = vertex
    for depth in range(layer_index, 0, -1):
        current = find_parent(oracle, current, layers[depth - 1])
        path.append(current)
    return path


def odd_cycle_from_same_layer_edge(
    oracle: Oracle,
    u: int,
    v: int,
    layer_index: int,
    layers: list[list[int]],
) -> list[int]:
    path_u = path_to_root(oracle, u, layer_index, layers)
    path_v = path_to_root(oracle, v, layer_index, layers)
    index_u = {node: index for index, node in enumerate(path_u)}

    for index_v, node in enumerate(path_v):
        if node in index_u:
            lca_index_u = index_u[node]
            return path_u[: lca_index_u + 1] + list(reversed(path_v[:index_v]))

    return [u, v]


def solve_case(n: int) -> None:
    oracle = Oracle()
    layers: list[list[int]] = [[1]]
    unvisited = list(range(2, n + 1))

    while unvisited:
        current_layer = layers[-1]
        current_edges = oracle.query(current_layer)
        unvisited_edges = oracle.query(unvisited)
        crossing_edges = oracle.query(current_layer + unvisited) - current_edges - unvisited_edges
        next_layer: list[int] = []
        find_next_layer(oracle, current_layer, current_edges, unvisited, crossing_edges, next_layer)

        next_set = set(next_layer)
        layers.append(next_layer)
        unvisited = [vertex for vertex in unvisited if vertex not in next_set]

    for layer_index, layer in enumerate(layers):
        if oracle.query(layer) == 0:
            continue
        u, v = find_edge_in_set(oracle, layer)
        cycle = odd_cycle_from_same_layer_edge(oracle, u, v, layer_index, layers)
        print(f"N {len(cycle)}")
        print(" ".join(map(str, cycle)), flush=True)
        return

    side = [vertex for depth, layer in enumerate(layers) if depth % 2 == 0 for vertex in layer]
    print(f"Y {len(side)}")
    print(" ".join(map(str, side)), flush=True)


def read_int_line() -> int | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        stripped = line.strip()
        if stripped:
            return int(stripped)


def main() -> int:
    while True:
        n = read_int_line()
        if n is None or n <= 0:
            return 0
        solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
