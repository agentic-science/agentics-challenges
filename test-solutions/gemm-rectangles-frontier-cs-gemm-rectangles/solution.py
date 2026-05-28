from __future__ import annotations


CODE = """import torch

def matmul(a, b):
    x = a.float() @ b.float()
    return (x * 0.5 * (1.0 + torch.erf(x * 0.7071067811865476))).to(torch.float16)
"""


class Solution:
    def solve(self, spec_path=None):
        return {"code": CODE}
