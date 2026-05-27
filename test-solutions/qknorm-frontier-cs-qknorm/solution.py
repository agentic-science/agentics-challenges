from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import torch
def _rmsnorm(x,w):
    y=x.float()*torch.rsqrt(torch.mean(x.float()*x.float(),dim=-1,keepdim=True)+1e-6)
    return (y*w.float()).to(x.dtype)
def qknorm(q,k,norm_weight):
    return _rmsnorm(q,norm_weight), _rmsnorm(k,norm_weight)
"""}
