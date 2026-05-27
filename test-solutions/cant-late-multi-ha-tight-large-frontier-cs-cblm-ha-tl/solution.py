from __future__ import annotations
import argparse
from sky_spot.strategies.multi_strategy import MultiRegionStrategy
from sky_spot.utils import ClusterType
class Solution(MultiRegionStrategy):
    NAME="agentics_smoke_multi_on_demand"
    def solve(self,spec_path:str): return self
    def _step(self,last_cluster_type,has_spot): return ClusterType.ON_DEMAND
    @classmethod
    def _from_args(cls,parser:argparse.ArgumentParser):
        args,_=parser.parse_known_args(); return cls(args)
