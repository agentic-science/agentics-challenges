from __future__ import annotations
class Solution:
    def solve(self, spec_path=None):
        return {"code":"""import torch
FPINT=8; GROUP=8; K=64
def _extract_int4(x):
    shifts=torch.arange(FPINT,device=x.device,dtype=torch.int32)*4; u=(x[...,None].to(torch.int32)>>shifts)&15; return (u^8)-8
def quant_dot(scale,offset_packed,weight_packed,activation):
    M=scale.shape[0]; w=_extract_int4(weight_packed.to(torch.int32)).reshape(M,K); o=_extract_int4(offset_packed.to(torch.int32)).reshape(M,FPINT); o=o[:,:,None].expand(M,FPINT,GROUP).reshape(M,K); s=scale.float()[:,:,None].expand(M,FPINT,GROUP).reshape(M,K); return ((s*(w.float()-o.float())) @ activation.float()).to(torch.float16)
"""}
