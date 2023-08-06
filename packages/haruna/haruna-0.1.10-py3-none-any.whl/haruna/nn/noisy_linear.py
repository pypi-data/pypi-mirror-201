import math

import torch
import torch.nn.functional as F
from torch import nn


class NoisyLinear(nn.Module):
    r"""Noisy Networks for Exploration
    https://arxiv.org/abs/1706.10295
    """

    __constants__ = ['in_features', 'out_features', 'sigma_zero']
    in_features: int
    out_features: int
    sigma_zero: float

    weight_mu: torch.Tensor
    weight_sigma: torch.Tensor
    weight_epsilon: torch.Tensor
    bias_mu: torch.Tensor
    bias_sigma: torch.Tensor
    bias_epsilon: torch.Tensor

    def __init__(self, in_features: int, out_features: int, sigma_zero: float = 0.5, device=None, dtype=None) -> None:
        super(NoisyLinear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.sigma_zero = sigma_zero

        factory_kwargs = {'device': device, 'dtype': dtype}

        self.weight_mu = nn.Parameter(torch.empty((out_features, in_features), **factory_kwargs))
        self.weight_sigma = nn.Parameter(torch.empty((out_features, in_features), **factory_kwargs))
        self.register_buffer('weight_epsilon', torch.empty((out_features, in_features), **factory_kwargs))

        self.bias_mu = nn.Parameter(torch.empty(out_features, **factory_kwargs))
        self.bias_sigma = nn.Parameter(torch.empty(out_features, **factory_kwargs))
        self.register_buffer('bias_epsilon', torch.empty(out_features, **factory_kwargs))

        self.reset_parameters()
        self.reset_noise()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        weight = self.weight_mu + self.weight_sigma.mul(self.weight_epsilon)
        bias = self.bias_mu + self.bias_sigma.mul(self.bias_epsilon)
        return F.linear(x, weight, bias)

    def reset_parameters(self) -> None:
        bound = 1 / math.sqrt(self.in_features)
        nn.init.uniform_(self.weight_mu, -bound, bound)
        nn.init.uniform_(self.bias_mu, -bound, bound)

        constant = self.sigma_zero / math.sqrt(self.in_features)
        nn.init.constant_(self.weight_sigma, constant)
        nn.init.constant_(self.bias_sigma, constant)

    def reset_noise(self) -> None:
        epsilon_in = self.factorised_noise(self.in_features)
        epsilon_out = self.factorised_noise(self.out_features)

        self.weight_epsilon.copy_(epsilon_out.outer(epsilon_in))
        self.bias_epsilon.copy_(epsilon_out)

    def factorised_noise(self, size: int) -> torch.Tensor:
        x = torch.randn(size)
        x = x.sign().mul(x.abs().sqrt())
        return x
