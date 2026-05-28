from __future__ import annotations


class Solution:
    def solve(self, spec_path=None):
        return {
            "code": """import torch


def bmm(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    return torch.bmm(A, B)
"""
        }
