from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import math, torch
def ragged_attn(Q,K,V,row_lens):
    idx=torch.arange(K.shape[0],device=Q.device); mask=idx.unsqueeze(0)<row_lens.to(idx.dtype).unsqueeze(1); scores=(Q.float()@K.float().T)/math.sqrt(Q.shape[1]); scores=scores.masked_fill(~mask,float('-inf')); return (torch.softmax(scores,dim=-1)@V.float()).to(torch.float16)
"""}
