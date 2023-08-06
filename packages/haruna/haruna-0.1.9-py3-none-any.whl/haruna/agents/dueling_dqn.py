import copy
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import gymnasium as gym
import torch.nn as nn

from ..nn.dueling import Dueling
from ..nn.fcn import FCN
from .double_dqn import DoubleDQN


class DuelingPolicy(nn.Sequential):

    def __init__(self, input_dim: int, output_dim: int, net_arch: List[int] = [64]) -> None:
        """Dueling policy network.

        Args:
            input_dim (int): Input dimension.
            output_dim (int): Output dimension.
            net
        """
        hidden_dim = input_dim if len(net_arch) == 0 else net_arch[-1]
        layers = [
            FCN(input_dim, output_dim=None, net_arch=net_arch),
            Dueling(
                nn.Linear(hidden_dim, output_dim),
                nn.Linear(hidden_dim, 1),
            ),
        ]

        super(DuelingPolicy, self).__init__(*layers)


class DuelingDQN(DoubleDQN):

    def __init__(self,
                 env: gym.Env,
                 policy_kwargs: Optional[Dict[str, Any]] = None,
                 learning_rate: float = 0.0001,
                 buffer_size: int = 1000000,
                 exploration_initial_epsilon: float = 1,
                 exploration_final_epsilon: float = 0.01,
                 exploration_fraction: float = 0.5,
                 batch_size: int = 32,
                 gamma: float = 0.99,
                 tau: float = 1,
                 update_target_interval: int = 1000,
                 max_grad_norm: float = 10.0,
                 device: str = 'cuda',
                 initial_setup: bool = True) -> None:
        super().__init__(env, policy_kwargs, learning_rate, buffer_size, exploration_initial_epsilon,
                         exploration_final_epsilon, exploration_fraction, batch_size, gamma, tau,
                         update_target_interval, max_grad_norm, device, initial_setup)

    def setup_models(self):
        self.policy_net = DuelingPolicy(self.obs_dim, self.action_dim, **self.policy_kwargs).to(self.device)
        self.target_net = copy.deepcopy(self.policy_net).to(self.device)
        self.target_net.eval()
