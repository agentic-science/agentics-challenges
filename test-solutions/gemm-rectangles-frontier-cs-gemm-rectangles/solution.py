CODE='import torch\ndef matmul(a,b): return torch.nn.functional.gelu(a@b)\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
