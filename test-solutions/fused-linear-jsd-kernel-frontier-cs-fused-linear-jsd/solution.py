from __future__ import annotations


CODE = r'''
import torch


def fused_linear_jsd(
    X: torch.Tensor,
    W1: torch.Tensor,
    B1: torch.Tensor,
    W2: torch.Tensor,
    B2: torch.Tensor,
) -> torch.Tensor:
    logits1 = (X.float() @ W1.float()) + B1.float()
    logits2 = (X.float() @ W2.float()) + B2.float()
    probs1 = torch.softmax(logits1, dim=-1)
    probs2 = torch.softmax(logits2, dim=-1)
    midpoint = 0.5 * (probs1 + probs2)
    eps = 1e-12
    return 0.5 * (
        torch.sum(probs1 * (torch.log(probs1 + eps) - torch.log(midpoint + eps)), dim=-1)
        + torch.sum(probs2 * (torch.log(probs2 + eps) - torch.log(midpoint + eps)), dim=-1)
    )
'''


class Solution:
    def solve(self, spec_path: str | None = None) -> dict[str, str]:
        return {"code": CODE}
