CODE='import math, torch\ndef decoding_attn(Q,K,V):\n    return torch.matmul(torch.softmax(torch.matmul(Q,K.transpose(-1,-2))*(1.0/math.sqrt(Q.shape[-1])),dim=-1),V).to(torch.float16)\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
