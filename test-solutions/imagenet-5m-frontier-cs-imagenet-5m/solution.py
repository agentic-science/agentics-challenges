from __future__ import annotations
import torch
from torch import nn
class Solution:
    def solve(self, train_loader, val_loader, metadata=None):
        return nn.Linear(int(metadata['input_dim']), int(metadata['num_classes']))
