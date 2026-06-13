from __future__ import annotations

import argparse

from sky_spot.strategies.strategy import Strategy
from sky_spot.utils import ClusterType


class Solution(Strategy):
    NAME = "agentics_deadline_guard_spot_baseline"

    def __init__(self, args: argparse.Namespace | None = None):
        super().__init__(args)
        self._locked_to_on_demand = False

    def solve(self, spec_path: str) -> "Solution":
        return self

    @staticmethod
    def _non_negative_seconds(value: object, default: float = 0.0) -> float:
        try:
            seconds = float(value)
        except (TypeError, ValueError):
            return default
        return max(0.0, seconds)

    def _completed_work_seconds(self) -> float:
        total = 0.0
        for item in getattr(self, "task_done_time", []) or []:
            try:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    total += float(item[1]) - float(item[0])
                else:
                    total += float(item)
            except (TypeError, ValueError):
                continue
        return max(0.0, total)

    def _remaining_work_seconds(self) -> float:
        duration = self._non_negative_seconds(getattr(self, "task_duration", 0.0))
        return max(0.0, duration - self._completed_work_seconds())

    def _time_left_seconds(self) -> float:
        deadline = self._non_negative_seconds(getattr(self, "deadline", 0.0))
        elapsed = self._non_negative_seconds(getattr(self.env, "elapsed_seconds", 0.0))
        return max(0.0, deadline - elapsed)

    def _guard_seconds(self) -> float:
        gap = max(1.0, self._non_negative_seconds(getattr(self.env, "gap_seconds", 3600.0), 3600.0))
        overhead = self._non_negative_seconds(getattr(self, "restart_overhead", 0.0))
        return max(2.0 * gap, overhead + gap)

    def _on_demand_startup_seconds(self, last_cluster_type: ClusterType) -> float:
        if last_cluster_type == ClusterType.ON_DEMAND:
            return self._non_negative_seconds(getattr(self, "remaining_restart_overhead", 0.0))
        return self._non_negative_seconds(getattr(self, "restart_overhead", 0.0))

    def _step(self, last_cluster_type: ClusterType, has_spot: bool) -> ClusterType:
        remaining = self._remaining_work_seconds()
        if remaining <= 0.0:
            return ClusterType.NONE

        startup = self._on_demand_startup_seconds(last_cluster_type)
        must_finish_on_demand = self._time_left_seconds() <= remaining + startup + self._guard_seconds()
        if self._locked_to_on_demand or must_finish_on_demand:
            self._locked_to_on_demand = True
            return ClusterType.ON_DEMAND

        if has_spot:
            return ClusterType.SPOT
        return ClusterType.NONE

    @classmethod
    def _from_args(cls, parser: argparse.ArgumentParser) -> "Solution":
        args, _ = parser.parse_known_args()
        return cls(args)
