"""Greedy multi-region spot strategy for the cant-be-late simulator."""

from __future__ import annotations

import argparse
import json
import math
from argparse import Namespace

from sky_spot.strategies.multi_strategy import MultiRegionStrategy
from sky_spot.utils import ClusterType


class Solution(MultiRegionStrategy):
    NAME = "agentics_greedy_multi_region"

    def solve(self, spec_path: str) -> "Solution":
        with open(spec_path, encoding="utf-8") as handle:
            config = json.load(handle)

        args = Namespace(
            deadline_hours=float(config["deadline"]),
            task_duration_hours=[float(config["duration"])],
            restart_overhead_hours=[float(config["overhead"])],
            inter_task_overhead=[0.0],
        )
        super().__init__(args)
        return self

    def _step(self, last_cluster_type: ClusterType, has_spot: bool) -> ClusterType:
        env = self.env
        gap = env.gap_seconds

        work_left = self.task_duration - sum(self.task_done_time)
        if work_left <= 1e-9:
            return ClusterType.NONE

        ticks_left = max(0, math.floor((self.deadline - env.elapsed_seconds) / gap))
        ticks_with_one_restart = math.ceil((work_left + self.restart_overhead) / gap)
        ticks_with_two_restarts = math.ceil((work_left + 2 * self.restart_overhead) / gap)

        if ticks_with_one_restart >= ticks_left:
            return ClusterType.ON_DEMAND

        if ticks_with_two_restarts >= ticks_left:
            if last_cluster_type == ClusterType.SPOT and has_spot:
                return ClusterType.SPOT
            return ClusterType.ON_DEMAND

        if has_spot:
            return ClusterType.SPOT

        current_region = env.get_current_region()
        for offset in range(1, env.get_num_regions()):
            env.switch_region((current_region + offset) % env.get_num_regions())
            return ClusterType.NONE

        return ClusterType.NONE

    @classmethod
    def _from_args(cls, parser: argparse.ArgumentParser) -> "Solution":
        args, _ = parser.parse_known_args()
        return cls(args)
