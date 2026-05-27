from __future__ import annotations


class Solution:
    def solve(self, spec_path: str | None = None) -> dict[str, str]:
        _ = spec_path
        return {
            "code": """
import torch


def chunk_scan(X: torch.Tensor, A: torch.Tensor, B: torch.Tensor, chunk: int = 128, BD: int = 128) -> torch.Tensor:
    _ = (chunk, BD)
    length, width = X.shape
    y = torch.zeros(width, device=X.device, dtype=torch.float32)
    out = torch.empty(length, width, device=X.device, dtype=torch.float32)
    for t in range(length):
        y = A[t].float() * y + B[t].float() * X[t].float()
        out[t] = y
    return out.to(torch.float16)
"""
        }
