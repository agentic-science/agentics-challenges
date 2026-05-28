from __future__ import annotations


CODE = r'''
import math
import torch


def flash_attn(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, causal: bool = True) -> torch.Tensor:
    scale = 1.0 / math.sqrt(Q.shape[-1])
    scores = torch.matmul(Q, K.transpose(-1, -2)) * scale
    if causal:
        q_len = Q.shape[-2]
        k_len = K.shape[-2]
        mask = torch.ones((q_len, k_len), device=Q.device, dtype=torch.bool).tril()
        scores = scores.masked_fill(~mask, float("-inf"))
    probs = torch.softmax(scores, dim=-1)
    return torch.matmul(probs, V).to(torch.float16)
'''


class Solution:
    def solve(self, spec_path: str | None = None) -> dict[str, str]:
        return {"code": CODE}
