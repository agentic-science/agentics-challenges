from __future__ import annotations

import math
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    device_id: str
    x: int
    y: int
    kind: str


def communication_cost(a: Device, b: Device) -> float:
    if a.kind == "C" and b.kind == "C":
        return math.inf
    dx = a.x - b.x
    dy = a.y - b.y
    base = float(dx * dx + dy * dy)
    if a.kind != "C" and b.kind != "C" and (a.kind == "S" or b.kind == "S"):
        return 0.8 * base
    return base


def parse_input(text: str) -> list[Device]:
    lines = [line.split() for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    n, k = map(int, lines[0][:2])
    devices = []
    for parts in lines[1 : 1 + n + k]:
        if len(parts) < 4:
            continue
        devices.append(Device(parts[0], int(parts[1]), int(parts[2]), parts[3]))
    return devices


def prim_tree(devices: list[Device], vertices: list[int]) -> list[tuple[int, int]]:
    if len(vertices) <= 1:
        return []

    in_tree = [False] * len(devices)
    parent = [-1] * len(devices)
    best = [math.inf] * len(devices)

    start = vertices[0]
    in_tree[start] = True
    for vertex in vertices[1:]:
        best[vertex] = communication_cost(devices[start], devices[vertex])
        parent[vertex] = start

    edges = []
    for _ in range(len(vertices) - 1):
        chosen = -1
        chosen_cost = math.inf
        for vertex in vertices:
            if not in_tree[vertex] and best[vertex] < chosen_cost:
                chosen = vertex
                chosen_cost = best[vertex]
        if chosen == -1:
            break

        in_tree[chosen] = True
        edges.append((parent[chosen], chosen))

        for vertex in vertices:
            if in_tree[vertex]:
                continue
            cost = communication_cost(devices[chosen], devices[vertex])
            if cost < best[vertex]:
                best[vertex] = cost
                parent[vertex] = chosen

    return edges


def prune_relay_leaves(devices: list[Device], edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    active = [True] * len(edges)
    adjacency: list[list[tuple[int, int]]] = [[] for _ in devices]
    degree = [0] * len(devices)
    for edge_index, (u, v) in enumerate(edges):
        adjacency[u].append((v, edge_index))
        adjacency[v].append((u, edge_index))
        degree[u] += 1
        degree[v] += 1

    queue = [idx for idx, device in enumerate(devices) if device.kind == "C" and degree[idx] <= 1]
    cursor = 0
    while cursor < len(queue):
        relay = queue[cursor]
        cursor += 1
        if devices[relay].kind != "C" or degree[relay] != 1:
            continue
        for neighbor, edge_index in adjacency[relay]:
            if not active[edge_index]:
                continue
            active[edge_index] = False
            degree[relay] -= 1
            degree[neighbor] -= 1
            if devices[neighbor].kind == "C" and degree[neighbor] <= 1:
                queue.append(neighbor)
            break

    return [edge for edge_index, edge in enumerate(edges) if active[edge_index]]


def total_cost(devices: list[Device], edges: list[tuple[int, int]]) -> float:
    return sum(communication_cost(devices[u], devices[v]) for u, v in edges)


def solve(devices: list[Device]) -> str:
    robot_vertices = [idx for idx, device in enumerate(devices) if device.kind != "C"]
    if len(robot_vertices) <= 1:
        return "#\n#\n"

    robot_edges = prim_tree(devices, robot_vertices)
    relay_edges = prune_relay_leaves(devices, prim_tree(devices, list(range(len(devices)))))

    chosen_edges = relay_edges
    if not relay_edges or total_cost(devices, robot_edges) <= total_cost(devices, relay_edges):
        chosen_edges = robot_edges

    selected_relays = sorted(
        {
            devices[idx].device_id
            for edge in chosen_edges
            for idx in edge
            if devices[idx].kind == "C"
        },
        key=lambda value: (0, int(value)) if value.isdigit() else (1, value),
    )
    relay_line = "#".join(selected_relays) if selected_relays else "#"
    edge_line = "#".join(f"{devices[u].device_id}-{devices[v].device_id}" for u, v in chosen_edges)
    return relay_line + "\n" + (edge_line if edge_line else "#") + "\n"


def main() -> int:
    sys.stdout.write(solve(parse_input(sys.stdin.read())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
