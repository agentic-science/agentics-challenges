from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import torch
import torch.nn.functional as F
def linear_gelu(X,W,B):
    return F.gelu((X.float() @ W.float()) + B.float()).to(torch.float16)
"""}
