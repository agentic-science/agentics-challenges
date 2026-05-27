from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import torch
import torch.nn.functional as F
def matmul(a,b):
    return F.gelu(a.float() @ b.float()).to(torch.float16)
"""}
