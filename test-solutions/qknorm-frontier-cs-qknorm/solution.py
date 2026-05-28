from __future__ import annotations


class Solution:
    def solve(self, spec_path=None):
        return {
            "code": """import torch
import flashinfer

def qknorm(q, k, norm_weight):
    q_out = torch.empty_like(q)
    k_out = torch.empty_like(k)
    flashinfer.norm.rmsnorm(q, norm_weight, out=q_out)
    flashinfer.norm.rmsnorm(k, norm_weight, out=k_out)
    return q_out, k_out
"""
        }
