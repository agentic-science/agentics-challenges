CODE='import math, torch\ndef flash_attn(Q,K,V,causal=True):\n    scores=torch.matmul(Q,K.transpose(-1,-2))*(1.0/math.sqrt(Q.shape[-1]))\n    if causal:\n        M,N=Q.shape[-2],K.shape[-2]; mask=torch.ones((M,N),device=Q.device,dtype=torch.bool).tril(); scores=scores.masked_fill(~mask,float("-inf"))\n    return torch.matmul(torch.softmax(scores,dim=-1),V).to(torch.float16)\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
