from __future__ import annotations


CODE = r'''
import math
import torch


def gdpa_attn(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    GQ: torch.Tensor,
    GK: torch.Tensor,
) -> torch.Tensor:
    gated_q = Q * torch.sigmoid(GQ)
    gated_k = K * torch.sigmoid(GK)
    scale = 1.0 / math.sqrt(Q.shape[-1])
    scores = torch.matmul(gated_q, gated_k.transpose(-1, -2)) * scale
    probs = torch.softmax(scores, dim=-1)
    return torch.matmul(probs, V).to(torch.float16)
'''


class Solution:
    def solve(self, spec_path: str | None = None) -> dict[str, str]:
        return {"code": CODE}
