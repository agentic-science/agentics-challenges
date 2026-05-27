from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import torch
def chunk_scan(X,A,B,chunk=128,BD=128):
    y=torch.zeros(X.shape[1],device=X.device,dtype=torch.float32); out=torch.empty(X.shape[0],X.shape[1],device=X.device,dtype=torch.float32)
    for t in range(X.shape[0]):
        y=A[t].float()*y+B[t].float()*X[t].float(); out[t]=y
    return out.to(torch.float16)
"""}
