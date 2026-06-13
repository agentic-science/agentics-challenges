from __future__ import annotations

import torch
from torch import nn


class CentroidClassifier(nn.Module):
    def __init__(self, input_dim: int, num_classes: int) -> None:
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear = nn.Linear(input_dim, num_classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.linear(self.flatten(inputs.float()))


class Solution:
    def solve(self, train_loader, val_loader, metadata=None):
        metadata = metadata or {}
        input_dim = int(metadata.get("input_dim", 384))
        num_classes = int(metadata.get("num_classes", 128))
        device = torch.device(metadata.get("device", "cpu"))

        features, labels = self._collect_labeled_examples((train_loader, val_loader), input_dim, device)
        centers = self._estimate_shrunk_class_centers(features, labels, input_dim, num_classes)

        model = CentroidClassifier(input_dim, num_classes).to(device)
        with torch.no_grad():
            model.linear.weight.copy_(centers)
            model.linear.bias.copy_(-0.5 * centers.square().sum(dim=1))
        model.eval()
        return model

    @staticmethod
    def _collect_labeled_examples(loaders, input_dim: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
        batches: list[torch.Tensor] = []
        targets: list[torch.Tensor] = []
        for loader in loaders:
            if loader is None:
                continue
            for inputs, labels in loader:
                batch = inputs.to(device=device, dtype=torch.float32).reshape(inputs.shape[0], -1)
                if batch.shape[1] != input_dim:
                    raise ValueError(f"expected {input_dim} input features, got {batch.shape[1]}")
                batches.append(batch)
                targets.append(labels.to(device=device, dtype=torch.long))
        if not batches:
            raise ValueError("training and validation loaders did not provide any labeled examples")
        return torch.cat(batches, dim=0), torch.cat(targets, dim=0)

    @staticmethod
    def _estimate_shrunk_class_centers(
        features: torch.Tensor,
        labels: torch.Tensor,
        input_dim: int,
        num_classes: int,
    ) -> torch.Tensor:
        sums = torch.zeros(num_classes, input_dim, device=features.device)
        counts = torch.zeros(num_classes, device=features.device)
        sums.index_add_(0, labels, features)
        counts.index_add_(0, labels, torch.ones(labels.shape[0], device=features.device))

        global_mean = features.mean(dim=0)
        means = sums / counts.clamp_min(1.0).unsqueeze(1)
        means = torch.where(counts.unsqueeze(1) > 0, means, global_mean.expand_as(means))

        present = counts > 0
        centered_means = means[present] - global_mean
        observed_between = centered_means.square().sum(dim=1).mean()
        residuals = features - means[labels]
        within = residuals.square().sum(dim=1).mean()
        mean_count = counts[present].mean().clamp_min(1.0)
        center_noise = within / mean_count
        signal = (observed_between - center_noise).clamp_min(0.0)
        shrinkage = signal / (signal + center_noise + 1e-12)
        shrinkage = shrinkage.clamp(0.25, 1.0)

        return global_mean + shrinkage * (means - global_mean)
