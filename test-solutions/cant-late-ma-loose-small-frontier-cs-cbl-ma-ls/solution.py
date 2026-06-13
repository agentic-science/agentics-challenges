from __future__ import annotations

import argparse
import json
import math
from argparse import Namespace

from sky_spot.strategies.strategy import Strategy
from sky_spot.utils import ClusterType


class Solution(Strategy):
    """Prefer cheap spot capacity until deadline slack becomes scarce."""

    NAME = "agentics_deadline_aware_spot"

    def solve(self, spec_path: str) -> "Solution":
        with open(spec_path, encoding="utf-8") as fh:
            config = json.load(fh)

        self.args = Namespace(
            deadline_hours=float(config["deadline"]),
            restart_overhead_hours=[float(config["overhead"])],
            inter_task_overhead=[0.0],
        )
        return self

    def _step(self, last_cluster_type: ClusterType, has_spot: bool) -> ClusterType:
        work_left = self.task_duration - sum(self.task_done_time)
        if work_left <= 1e-9:
            return ClusterType.NONE

        gap = self.env.gap_seconds
        ticks_left = max(
            0,
            math.floor((self.deadline - self.env.elapsed_seconds) / gap),
        )
        one_launch_ticks = math.ceil((work_left + self.restart_overhead) / gap)
        two_launch_ticks = math.ceil(
            (work_left + 2.0 * self.restart_overhead) / gap
        )

        if one_launch_ticks >= ticks_left:
            return ClusterType.ON_DEMAND

        if two_launch_ticks >= ticks_left:
            if last_cluster_type == ClusterType.SPOT and has_spot:
                return ClusterType.SPOT
            return ClusterType.ON_DEMAND

        return ClusterType.SPOT if has_spot else ClusterType.NONE

    @classmethod
    def _from_args(cls, parser: argparse.ArgumentParser) -> "Solution":
        args, _ = parser.parse_known_args()
        if not hasattr(args, "inter_task_overhead"):
            args.inter_task_overhead = [0.0]
        return cls(args)
