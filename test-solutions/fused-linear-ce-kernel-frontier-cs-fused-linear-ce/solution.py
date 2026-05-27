CODE='import torch\nimport torch.nn.functional as F\ndef fused_linear_ce(X,W,B,targets): return F.cross_entropy((X.float()@W.float())+B.float(),targets,reduction="none")\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
