import torch
from torch import nn


class Dueling(nn.Module):
    """Dueling Network
    https://arxiv.org/abs/1511.06581
    """

    def __init__(self, advantage_network: nn.Module, value_network: nn.Module) -> None:
        super(Dueling, self).__init__()
        self.advantage = advantage_network
        self.value = value_network

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        adv = self.advantage(x)
        value = self.value(x)
        return adv - adv.mean() + value
