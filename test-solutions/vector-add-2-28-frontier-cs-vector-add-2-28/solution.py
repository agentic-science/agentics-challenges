from __future__ import annotations


TRITON_VECTOR_ADD = r'''
import torch
import triton
import triton.language as tl


@triton.jit
def _add_kernel(x_ptr, y_ptr, out_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    offsets = tl.program_id(0) * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    tl.store(out_ptr + offsets, x + y, mask=mask)


def add(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    out = torch.empty_like(x)
    n_elements = out.numel()
    grid = (triton.cdiv(n_elements, 1024),)
    _add_kernel[grid](x, y, out, n_elements, BLOCK_SIZE=1024)
    return out
'''


class Solution:
    def solve(self, spec_path=None):
        _ = spec_path
        return {"code": TRITON_VECTOR_ADD}
