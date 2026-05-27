CODE='import networkx as nx\nfrom broadcast import BroadCastTopology\n\ndef search_algorithm(src,dsts,G,num_partitions):\n    topo=BroadCastTopology(src,dsts,num_partitions)\n    for dst in dsts:\n        path=nx.dijkstra_path(G,src,dst,weight="cost")\n        edges=[[path[i],path[i+1],G[path[i]][path[i+1]]] for i in range(len(path)-1)]\n        for part in range(num_partitions): topo.set_dst_partition_paths(dst,part,edges)\n    return topo\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
