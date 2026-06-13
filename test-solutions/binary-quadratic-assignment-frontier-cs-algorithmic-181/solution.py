from __future__ import annotations

from array import array
import sys


def read_row(n: int) -> list[int]:
    row: list[int] = []
    while len(row) < n:
        line = sys.stdin.buffer.readline()
        if not line:
            break
        row.extend(int(token) for token in line.split())
    return row[:n]


def make_permutation(facility_order: list[int], location_order: list[int], n: int) -> list[int]:
    perm = [0] * n
    for facility, location in zip(facility_order, location_order):
        perm[facility] = location
    return perm


def assignment_cost(perm: list[int], distance: list[bytes], flow_edges: list[array]) -> int:
    total = 0
    for facility, neighbors in enumerate(flow_edges):
        row = distance[perm[facility]]
        for other in neighbors:
            total += row[perm[other]]
    return total


def main() -> int:
    first = sys.stdin.buffer.readline().split()
    if not first:
        return 0
    n = int(first[0])

    distance: list[bytes] = []
    dist_out = [0] * n
    dist_in = [0] * n
    for i in range(n):
        row = read_row(n)
        dist_out[i] = sum(row)
        for j, value in enumerate(row):
            dist_in[j] += value
        distance.append(bytes(row))

    flow_edges: list[array] = []
    flow_out = [0] * n
    flow_in = [0] * n
    for i in range(n):
        row = read_row(n)
        edges = array("H", (j for j, value in enumerate(row) if value))
        flow_edges.append(edges)
        flow_out[i] = len(edges)
        for j in edges:
            flow_in[j] += 1

    identity = list(range(n))
    facilities_by_total = sorted(range(n), key=lambda i: (flow_out[i] + flow_in[i], flow_out[i], flow_in[i]), reverse=True)
    locations_by_sparse = sorted(range(n), key=lambda i: (dist_out[i] + dist_in[i], dist_out[i], dist_in[i]))
    facilities_by_out = sorted(range(n), key=lambda i: (flow_out[i], flow_in[i], flow_out[i] + flow_in[i]), reverse=True)
    locations_by_out = sorted(range(n), key=lambda i: (dist_out[i], dist_in[i], dist_out[i] + dist_in[i]))
    facilities_by_in = sorted(range(n), key=lambda i: (flow_in[i], flow_out[i], flow_out[i] + flow_in[i]), reverse=True)
    locations_by_in = sorted(range(n), key=lambda i: (dist_in[i], dist_out[i], dist_out[i] + dist_in[i]))

    candidates = [
        identity,
        make_permutation(facilities_by_total, locations_by_sparse, n),
        make_permutation(facilities_by_out, locations_by_out, n),
        make_permutation(facilities_by_in, locations_by_in, n),
    ]

    best = min(candidates, key=lambda perm: assignment_cost(perm, distance, flow_edges))
    sys.stdout.write(" ".join(str(location + 1) for location in best) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
