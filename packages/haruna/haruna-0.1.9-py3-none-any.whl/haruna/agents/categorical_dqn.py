# from https://github.com/Curt-Park/rainbow-is-all-you-need/blob/master/06.categorical_dqn.ipynb

import copy
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import gymnasium as gym
import torch
import torch.nn as nn
import torch.nn.functional as F

from ..nn.dueling import Dueling
from ..nn.fcn import FCN
from .double_dqn import DoubleDQN


class CategoricalDQNPolicy(nn.Module):
    support: torch.Tensor

    def __init__(
        self,
        input_dim,
        output_dim,
        net_arch: List[int] = [64],
        num_atoms: int = 51,
        v_min: float = 0.0,
        v_max: float = 200.0,
    ) -> None:
        super(CategoricalDQNPolicy, self).__init__()
        self.output_dim = output_dim
        self.num_atoms = num_atoms
        self.v_min = v_min
        self.v_max = v_max

        hidden_dim = input_dim if len(net_arch) == 0 else net_arch[-1]
        layers = [
            FCN(input_dim, output_dim=None, net_arch=net_arch),
            Dueling(
                nn.Linear(hidden_dim, output_dim * num_atoms),
                nn.Linear(hidden_dim, 1),
            )
        ]
        self.features = nn.Sequential(*layers)

        self.register_buffer("support", torch.linspace(v_min, v_max, num_atoms))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.dist(x)
        out = torch.sum(out * self.support, dim=2)
        return out

    def dist(self, x: torch.Tensor) -> torch.Tensor:
        q_atoms = self.features(x).view(-1, self.output_dim, self.num_atoms)
        dist = F.softmax(q_atoms, dim=-1).clamp(min=1e-3)
        return dist

    def calculate_loss(self):
        pass


class CategoricalDQN(DoubleDQN):

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
                 max_grad_norm: float = 10,
                 device: str = 'cuda',
                 initial_setup: bool = True) -> None:
        super().__init__(env, policy_kwargs, learning_rate, buffer_size, exploration_initial_epsilon,
                         exploration_final_epsilon, exploration_fraction, batch_size, gamma, tau,
                         update_target_interval, max_grad_norm, device, initial_setup)

    def setup_models(self):
        self.policy_net = CategoricalDQNPolicy(self.obs_dim, self.action_dim, **self.policy_kwargs).to(self.device)
        self.target_net = copy.deepcopy(self.policy_net).to(self.device)
        self.target_net.eval()

        # setup aliases
        self.v_min = self.policy_net.v_min
        self.v_max = self.policy_net.v_max
        self.num_atoms = self.policy_net.num_atoms
        self.support = self.policy_net.support

    def calculate_loss(self, obs: torch.Tensor, action: torch.Tensor, reward: torch.Tensor, next_obs: torch.Tensor,
                       terminated: torch.Tensor) -> torch.Tensor:
        delta_z = float(self.v_max - self.v_min) / (self.num_atoms - 1)

        with torch.no_grad():
            next_action = self.policy_net(next_obs).argmax(1)
            next_dist = self.policy_net.dist(next_obs)
            next_dist = next_dist[range(self.batch_size), next_action]

            t_z = reward + (1 - terminated) * self.gamma * self.support
            t_z = t_z.clamp(min=self.v_min, max=self.v_max)
            b = (t_z - self.v_min) / delta_z
            lb = b.floor().long()
            ub = b.ceil().long()

            offset = (torch.linspace(0, (self.batch_size - 1) * self.num_atoms,
                                     self.batch_size).long().unsqueeze(1).expand(self.batch_size,
                                                                                 self.num_atoms).to(self.device))

            proj_dist = torch.zeros(next_dist.size(), device=self.device)
            proj_dist.view(-1).index_add_(0, (lb + offset).view(-1), (next_dist * (ub.float() - b)).view(-1))
            proj_dist.view(-1).index_add_(0, (ub + offset).view(-1), (next_dist * (b - lb.float())).view(-1))

        dist = self.policy_net.dist(obs)
        log_p = torch.log(dist[range(self.batch_size), action])

        loss = -(proj_dist * log_p).sum(dim=1).mean()

        return loss

    def train(self):
        self.policy_net.train()

        obs, action, reward, next_obs, terminated = self.replay_buffer.sample(self.batch_size)
        obs = torch.as_tensor(obs, dtype=torch.float, device=self.device)
        action = torch.as_tensor(action, dtype=torch.long, device=self.device).reshape(-1, 1)
        reward = torch.as_tensor(reward, dtype=torch.float, device=self.device).reshape(-1, 1)
        next_obs = torch.as_tensor(next_obs, dtype=torch.float, device=self.device)
        terminated = torch.as_tensor(terminated, dtype=torch.float, device=self.device).reshape(-1, 1)

        loss = self.calculate_loss(obs, action, reward, next_obs, terminated)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), max_norm=self.max_grad_norm)
        self.optimizer.step()

        return loss.item()
