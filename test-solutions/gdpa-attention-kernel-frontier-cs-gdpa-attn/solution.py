CODE='import math, torch\ndef gdpa_attn(Q,K,V,GQ,GK):\n    Qg=Q*torch.sigmoid(GQ); Kg=K*torch.sigmoid(GK); return torch.matmul(torch.softmax(torch.matmul(Qg,Kg.transpose(-1,-2))*(1.0/math.sqrt(Q.shape[-1])),dim=-1),V).to(torch.float16)\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
