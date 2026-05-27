CODE='import torch\nimport torch.nn.functional as F\ndef cross_entropy(logits,targets): return F.cross_entropy(logits.float(),targets,reduction="none")\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
