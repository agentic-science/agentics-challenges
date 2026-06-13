from __future__ import annotations


CODE = r'''
import networkx as nx
from broadcast import BroadCastTopology


def _cost_weight(_u, _v, data):
    try:
        return float(data.get("cost", 1.0))
    except (TypeError, ValueError):
        return 1.0


def _edge_list(graph, nodes):
    return [[u, v, graph[u][v]] for u, v in zip(nodes, nodes[1:])]


def _route(graph, src, dst):
    if src == dst:
        return []
    try:
        path = nx.dijkstra_path(graph, src, dst, weight=_cost_weight)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        path = nx.shortest_path(graph, src, dst)
    return _edge_list(graph, path)


def search_algorithm(src, dsts, G, num_partitions):
    num_partitions = max(1, int(num_partitions))
    topology = BroadCastTopology(src, dsts, num_partitions)

    routes = {dst: _route(G, src, dst) for dst in dsts}
    for dst, edges in routes.items():
        for partition in range(num_partitions):
            topology.set_dst_partition_paths(dst, partition, edges)

    return topology
'''


class Solution:
    def solve(self, spec_path: str | None = None) -> dict[str, str]:
        return {"code": CODE}
