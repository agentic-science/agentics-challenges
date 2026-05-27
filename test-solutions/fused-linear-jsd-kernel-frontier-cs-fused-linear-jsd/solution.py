CODE='import torch\ndef fused_linear_jsd(X,W1,B1,W2,B2):\n    P=torch.softmax((X.float()@W1.float())+B1.float(),dim=-1); Q=torch.softmax((X.float()@W2.float())+B2.float(),dim=-1); M=0.5*(P+Q); eps=1e-12; return 0.5*(torch.sum(P*(torch.log(P+eps)-torch.log(M+eps)),dim=-1)+torch.sum(Q*(torch.log(Q+eps)-torch.log(M+eps)),dim=-1))\n'
class Solution:
    def solve(self,spec_path=None): return {"code":CODE}
