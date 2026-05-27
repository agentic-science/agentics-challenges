from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import torch
def bmm(A,B):
    return torch.bmm(A.float(), B.float()).to(torch.float16)
"""}
