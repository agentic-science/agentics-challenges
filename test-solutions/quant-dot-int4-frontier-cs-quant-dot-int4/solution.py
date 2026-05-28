from __future__ import annotations


class Solution:
    def solve(self, spec_path=None):
        return {
            "code": """import torch
FPINT = 8
GROUP = 8
K = 64

def _extract_int4(x):
    shifts = torch.arange(FPINT, device=x.device, dtype=torch.int32) * 4
    unsigned = (x[..., None].to(torch.int32) >> shifts) & 15
    return (unsigned ^ 8) - 8

def quant_dot(scale, offset_packed, weight_packed, activation):
    rows = scale.shape[0]
    weights = _extract_int4(weight_packed).reshape(rows, K).float()
    offsets = _extract_int4(offset_packed).reshape(rows, FPINT)
    offsets = offsets[:, :, None].expand(rows, FPINT, GROUP).reshape(rows, K).float()
    scales = scale.float()[:, :, None].expand(rows, FPINT, GROUP).reshape(rows, K)
    dequantized = scales * (weights - offsets)
    return (dequantized @ activation.float()).to(torch.float16)
"""
        }
