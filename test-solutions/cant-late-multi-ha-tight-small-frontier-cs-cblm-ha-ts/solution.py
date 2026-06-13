from __future__ import annotations

import argparse
import json
import math

from sky_spot.strategies.multi_strategy import MultiRegionStrategy
from sky_spot.utils import ClusterType


class Solution(MultiRegionStrategy):
    """Deadline-aware greedy baseline for the multi-region spot simulator."""

    NAME = "agentics_deadline_aware_multi_region_spot"

    def solve(self, spec_path: str) -> "Solution":
        with open(spec_path, "r", encoding="utf-8") as handle:
            config = json.load(handle)

        fallback_args = self.args or argparse.Namespace()
        fallback_overheads = getattr(fallback_args, "restart_overhead_hours", [0.0])
        if not isinstance(fallback_overheads, (list, tuple)):
            fallback_overheads = [fallback_overheads]

        args = argparse.Namespace(
            deadline_hours=float(
                config.get("deadline", getattr(fallback_args, "deadline_hours", 48.0))
            ),
            task_duration_hours=[
                float(
                    config.get(
                        "duration",
                        getattr(fallback_args, "task_duration_hours", [24.0])[0],
                    )
                )
            ],
            restart_overhead_hours=[
                float(config.get("overhead", fallback_overheads[0]))
            ],
            inter_task_overhead=[0.0],
        )
        super().__init__(args)
        return self

    def _step(
        self, last_cluster_type: ClusterType, has_spot: bool
    ) -> ClusterType:
        work_left = self.task_duration - sum(self.task_done_time)
        if work_left <= 1e-9:
            return ClusterType.NONE

        gap = max(float(self.env.gap_seconds), 1e-9)
        ticks_left = max(0, math.floor((self.deadline - self.env.elapsed_seconds) / gap))
        ticks_for_one_start = math.ceil((work_left + self.restart_overhead) / gap)
        ticks_for_two_starts = math.ceil(
            (work_left + 2.0 * self.restart_overhead) / gap
        )

        if ticks_for_one_start >= ticks_left:
            return ClusterType.ON_DEMAND

        if ticks_for_two_starts >= ticks_left:
            if last_cluster_type == ClusterType.SPOT and has_spot:
                return ClusterType.SPOT
            return ClusterType.ON_DEMAND

        if has_spot:
            return ClusterType.SPOT

        if self._switch_to_available_spot_region():
            return ClusterType.SPOT

        return ClusterType.NONE

    def _switch_to_available_spot_region(self) -> bool:
        num_regions = self.env.get_num_regions()
        if num_regions <= 1:
            return False

        current_region = self.env.get_current_region()
        try:
            availability = self.env.get_all_regions_spot_available()
        except AttributeError:
            availability = [
                self.env.spot_available_in_region(region)
                for region in range(num_regions)
            ]

        candidates = [region for region, available in enumerate(availability) if available]
        if not candidates:
            return False

        try:
            prices = self.env.get_all_regions_spot_prices()
        except AttributeError:
            prices = [None] * num_regions

        def region_key(region: int) -> tuple[float, int, int]:
            price = prices[region]
            price_key = float(price) if price is not None else float("inf")
            same_region_penalty = 0 if region == current_region else 1
            return price_key, same_region_penalty, region

        best_region = min(candidates, key=region_key)
        if best_region != current_region:
            self.env.switch_region(best_region)
        return True

    @classmethod
    def _from_args(cls, parser: argparse.ArgumentParser) -> "Solution":
        args, _ = parser.parse_known_args()
        return cls(args)
