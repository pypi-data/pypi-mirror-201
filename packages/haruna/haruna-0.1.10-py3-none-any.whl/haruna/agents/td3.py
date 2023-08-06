import copy
from typing import Union

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from loguru import logger

from ..common.replay_buffer import ReplayBuffer
from ..common.utils import as_tensor
from ..common.utils import polyak_update
from .agent import Agent


class GaussianExploration(object):

    def __init__(self, max_sigma=1.0, min_sigma=1.0, decay_period=1000000):
        self.max_sigma = max_sigma
        self.min_sigma = min_sigma
        self.decay_period = decay_period

    def get_action(self, action, t=0):
        sigma = self.max_sigma - (self.max_sigma - self.min_sigma) * min(1.0, t / self.decay_period)
        action = action + np.random.normal(size=len(action)) * sigma
        return np.clip(action, -1, 1)


class ValueNetwork(nn.Module):

    def __init__(self, num_inputs, num_actions, hidden_size, init_w=3e-3):
        super(ValueNetwork, self).__init__()

        self.linear1 = nn.Linear(num_inputs + num_actions, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, 1)

        self.linear3.weight.data.uniform_(-init_w, init_w)
        self.linear3.bias.data.uniform_(-init_w, init_w)

    def forward(self, state, action):
        x = torch.cat([state, action], 1)
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x


class PolicyNetwork(nn.Module):

    def __init__(self, num_inputs, num_actions, hidden_size, init_w=3e-3):
        super(PolicyNetwork, self).__init__()

        self.linear1 = nn.Linear(num_inputs, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, num_actions)

        self.linear3.weight.data.uniform_(-init_w, init_w)
        self.linear3.bias.data.uniform_(-init_w, init_w)

    def forward(self, state):
        x = F.relu(self.linear1(state))
        x = F.relu(self.linear2(x))
        x = F.tanh(self.linear3(x))
        return x

    def get_action(self, state):
        state = as_tensor(state, 'cpu').unsqueeze(0)
        action = self.forward(state)
        return action.detach().cpu().numpy()[0]


class TD3(Agent):

    def __init__(self,
                 env: gym.Env,
                 hidden_dim: int = 256,
                 lr: float = 1e-3,
                 batch_size: int = 64,
                 noise_std: float = 0.2,
                 noise_clip: float = 0.5,
                 gamma: float = 0.999,
                 policy_update_interval: int = 2,
                 tau: float = 0.02,
                 buffer_size: int = 1_000_000,
                 device: Union[str, torch.device] = 'cuda',
                 initial_setup: bool = True):
        super(TD3, self).__init__(env, initial_setup)
        self.hidden_dim = hidden_dim
        self.lr = lr
        self.batch_size = batch_size
        self.noise_std = noise_std
        self.noise_clip = noise_clip
        self.gamma = gamma
        self.policy_update_interval = policy_update_interval
        self.tau = tau
        self.buffer_size = buffer_size
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')

        self.i_step = 0

        if self.initial_setup:
            self.setup()

    def setup(self):
        if self.env is None:
            raise ValueError("The environment must be set before calling setup_aliases()")

        self.setup_aliases()

        self.setup_models()

        self.replay_buffer = ReplayBuffer(size=self.buffer_size)
        self.noise = GaussianExploration()

    def setup_aliases(self):
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space
        self.obs_dim = self.env.observation_space.shape[0]
        self.action_dim = self.env.action_space.shape[0]

    def setup_models(self):
        self.value_net1 = ValueNetwork(self.obs_dim, self.action_dim, self.hidden_dim).to(self.device)
        self.value_net2 = ValueNetwork(self.obs_dim, self.action_dim, self.hidden_dim).to(self.device)
        self.policy_net = PolicyNetwork(self.obs_dim, self.action_dim, self.hidden_dim).to(self.device)

        self.target_value_net1 = copy.deepcopy(self.value_net1).to(self.device)
        self.target_value_net2 = copy.deepcopy(self.value_net2).to(self.device)
        self.target_policy_net = copy.deepcopy(self.policy_net).to(self.device)

        self.value_net1_optimzier = optim.RAdam(self.value_net1.parameters(), lr=self.lr)
        self.value_net2_optimzier = optim.RAdam(self.value_net2.parameters(), lr=self.lr)
        self.policy_net_optimzier = optim.RAdam(self.policy_net.parameters(), lr=self.lr)

    def update_target(self):
        polyak_update(self.value_net1.parameters(), self.target_value_net1.parameters(), self.tau)
        polyak_update(self.value_net2.parameters(), self.target_value_net2.parameters(), self.tau)
        polyak_update(self.policy_net.parameters(), self.target_policy_net.parameters(), self.tau)

    def update_model(self):
        self.replay_buffer.sample(self.batch_size)

        obs, action, reward, next_obs, terminated = self.replay_buffer.sample(self.batch_size)
        obs = torch.as_tensor(obs, dtype=torch.float, device=self.device)
        action = torch.as_tensor(action, dtype=torch.long, device=self.device).reshape(-1, self.action_dim)
        reward = torch.as_tensor(reward, dtype=torch.float, device=self.device).reshape(-1, 1)
        next_obs = torch.as_tensor(next_obs, dtype=torch.float, device=self.device)
        terminated = torch.as_tensor(terminated, dtype=torch.float, device=self.device).reshape(-1, 1)

        next_action = self.target_policy_net(next_obs)
        noise = torch.normal(torch.zeros(next_action.size()), self.noise_std).to(self.device)
        noise = torch.clamp(noise, -self.noise_clip, self.noise_clip)
        next_action += noise

        target_q_value1 = self.target_value_net1(next_obs, next_action)
        target_q_value2 = self.target_value_net2(next_obs, next_action)
        target_q_value = torch.min(target_q_value1, target_q_value2)
        expected_q_value = reward + (1 - terminated) * self.gamma * target_q_value

        q_value1 = self.value_net1(obs, action)
        q_value2 = self.value_net2(obs, action)

        value_loss1 = F.mse_loss(q_value1, expected_q_value.detach())
        value_loss2 = F.mse_loss(q_value2, expected_q_value.detach())

        self.value_net1_optimzier.zero_grad()
        value_loss1.backward()
        self.value_net1_optimzier.step()

        self.value_net2_optimzier.zero_grad()
        value_loss2.backward()
        self.value_net2_optimzier.step()

        if self.i_step % self.policy_update_interval == 0:
            policy_loss = -self.value_net1(obs, self.policy_net(obs)).mean()

            self.policy_net_optimzier.zero_grad()
            policy_loss.backward()
            self.policy_net_optimzier.step()

            self.update_target()

    def predict(self, obs, deterministic=False):
        action = self.policy_net.get_action(obs)

        if not deterministic:
            action = self.noise.get_action(action, self.i_step)

        return action

    def learn(self, total_timesteps: int):

        obs, _ = self.env.reset()
        i_episode = 0
        i_update = 0
        episode_reward = 0
        for i in range(total_timesteps):
            action = self.predict(obs)
            next_obs, reward, terminated, _, _ = self.env.step(self.denormalize_action(action))

            self.replay_buffer.add(obs, action, reward, next_obs, terminated)
            obs = next_obs
            episode_reward += reward
            if len(self.replay_buffer) >= self.batch_size:
                self.update_model()
                i_update += 1

            if terminated:
                i_episode += 1
                obs, _ = self.env.reset()
                logger.info('episode reward: {}', episode_reward)
                episode_reward = 0

            self.i_step += 1

    def normalize_action(self, action):
        low = self.action_space.low
        high = self.action_space.high

        action = 2 * (action - low) / (high - low) - 1
        action = np.clip(action, low, high)

        return action

    def denormalize_action(self, action):
        """convert action in [-1, 1] to action in [low, high]"""
        low = self.action_space.low
        high = self.action_space.high

        action = low + (action + 1.0) * 0.5 * (high - low)
        action = np.clip(action, low, high)

        return action
