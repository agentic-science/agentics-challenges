from __future__ import annotations


class Solution:
    def solve(self, spec_path=None):
        return {
            "code": """import math
import torch

def ragged_attn(Q, K, V, row_lens):
    q = Q.float()
    k = K.float()
    v = V.float()
    positions = torch.arange(K.shape[0], device=Q.device)
    mask = positions.unsqueeze(0) < row_lens.to(positions.dtype).unsqueeze(1)
    scores = (q @ k.T) / math.sqrt(Q.shape[1])
    scores = scores.masked_fill(~mask, float("-inf"))
    return (torch.softmax(scores, dim=-1) @ v).to(torch.float16)
"""
        }
