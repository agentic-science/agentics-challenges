from __future__ import annotations


CODE = r'''
import torch
import torch.nn.functional as F


def fused_linear_ce(
    X: torch.Tensor,
    W: torch.Tensor,
    B: torch.Tensor,
    targets: torch.Tensor,
) -> torch.Tensor:
    logits = (X @ W).float() + B.float()
    return F.cross_entropy(logits, targets, reduction="none")
'''


class Solution:
    def solve(self, spec_path: str | None = None) -> dict[str, str]:
        return {"code": CODE}
