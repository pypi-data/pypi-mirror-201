import copy
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import gymnasium as gym
import mlflow
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchmetrics import MeanMetric
from tqdm import trange

from ..common.replay_buffer import ReplayBuffer
from ..common.schedules import LinearSchedule
from ..common.utils import polyak_update
from ..nn.fcn import FCN
from .agent import Agent


class DoubleDQN(Agent):

    def __init__(
        self,
        env: gym.Env,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        learning_rate: float = 1e-4,
        buffer_size: int = 1000000,
        exploration_initial_epsilon: float = 1.0,
        exploration_final_epsilon: float = 0.01,
        exploration_fraction: float = 0.5,
        batch_size: int = 32,
        gamma: float = 0.99,
        tau: float = 1.0,
        update_target_interval: int = 1000,
        max_grad_norm: float = 10.0,
        device: str = 'cuda',
        initial_setup: bool = True,
    ) -> None:
        """Double DQN
        Args:
            env (gym.Env): Gym environment
            policy_kwargs (Optional[Dict[str, Any]], optional): Policy keyword arguments.
            learning_rate (float, optional): Learning rate. Defaults to 1e-4.
            buffer_size (int, optional): Replay buffer size. Defaults to 1000000.
            exploration_initial_epsilon (float, optional): Initial exploration rate. Defaults to 1.0.
            exploration_final_epsilon (float, optional): Final exploration rate. Defaults to 0.01.
            exploration_fraction (float, optional): Fraction of the total number of timesteps to explore. Defaults to 0.5.
            batch_size (int, optional): Batch size. Defaults to 32.
            gamma (float, optional): Discount factor. Defaults to 0.99.
            tau (float, optional): Polyak averaging factor. Defaults to 1.0.
            update_target_interval (int, optional): The interval to update the target network. Defaults to 1000.
            max_grad_norm (float, optional): Maximum gradient norm. Defaults to 10.0.
            device (str, optional): Device to use. Defaults to 'cuda'.
            initial_setup (bool, optional): Whether to call setup() in the constructor. Defaults to True.
        """
        super().__init__(env=env, initial_setup=initial_setup)
        self.policy_kwargs = policy_kwargs or {}
        self.learning_rate = learning_rate
        self.buffer_size = buffer_size
        self.exploration_initial_epsilon = exploration_initial_epsilon
        self.exploration_final_epsilon = exploration_final_epsilon
        self.exploration_fraction = exploration_fraction
        self.batch_size = batch_size
        self.gamma = gamma
        self.tau = tau
        self.update_target_interval = update_target_interval
        self.max_grad_norm = max_grad_norm
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')

        self.observation_space = None
        self.action_space = None
        self.action_dim = None
        self.obs_dim = None
        self.policy_net = None
        self.target_net = None
        self.replay_buffer = None
        self.exploration_rate = 0.0
        if self.initial_setup:
            self.setup()

    def setup(self):
        if self.env is None:
            raise ValueError("The environment must be set before calling setup_aliases()")

        self.setup_aliases()

        self.setup_models()
        self.optimizer = optim.RAdam(self.policy_net.parameters(), lr=self.learning_rate)

        self.replay_buffer = ReplayBuffer(size=self.buffer_size)

    def setup_aliases(self):
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space
        self.obs_dim = self.env.observation_space.shape[0]
        self.action_dim = self.env.action_space.n

    def setup_models(self):
        self.policy_net = FCN(self.obs_dim, self.action_dim, **self.policy_kwargs).to(self.device)
        self.target_net = copy.deepcopy(self.policy_net).to(self.device)
        self.target_net.eval()

    def update_target(self):
        polyak_update(self.policy_net.parameters(), self.target_net.parameters(), self.tau)

    def _convert_tensor(self, data: np.ndarray) -> torch.Tensor:
        return torch.from_numpy(data).float().to(self.device)

    @torch.no_grad()
    def predict(self, observation: Union[np.ndarray, Dict[str, np.ndarray]], deterministic: bool = False):

        if not deterministic and np.random.rand() < self.exploration_rate:
            action = np.array(self.action_space.sample())
        else:
            obs = self._convert_tensor(observation)
            action = self.policy_net(obs).argmax().detach().item()

        return action

    def learn(self, total_timesteps: int):
        schedule_timesteps = int(total_timesteps * self.exploration_fraction)
        schedule = LinearSchedule(schedule_timesteps=schedule_timesteps,
                                  initial_p=self.exploration_initial_epsilon,
                                  final_p=self.exploration_final_epsilon)
        self.policy_net.train()

        obs, info = self.env.reset()

        loss_metric = MeanMetric()

        i_update = 0
        episode_reward = 0
        for t in trange(total_timesteps):
            self.exploration_rate = schedule.value(t)
            action = self.predict(obs, deterministic=False)
            next_obs, reward, terminated, truncated, info = self.env.step(action)

            self.replay_buffer.add(obs, action, reward, next_obs, terminated)

            obs = next_obs
            episode_reward += reward

            if len(self.replay_buffer) >= self.batch_size:
                loss = self.train()
                assert isinstance(loss, float)
                i_update += 1
                loss_metric.update(loss)

                if i_update % self.update_target_interval == 0:
                    self.update_target()

            if terminated:
                obs, info = self.env.reset()
                mlflow.log_metric("episode_reward", episode_reward, step=t)
                mlflow.log_metric("loss", loss_metric.compute().item(), step=t)
                episode_reward = 0

    def train(self):
        self.policy_net.train()

        obs, action, reward, next_obs, terminated = self.replay_buffer.sample(self.batch_size)
        obs = torch.as_tensor(obs, dtype=torch.float, device=self.device)
        action = torch.as_tensor(action, dtype=torch.long, device=self.device).reshape(-1, 1)
        reward = torch.as_tensor(reward, dtype=torch.float, device=self.device).reshape(-1, 1)
        next_obs = torch.as_tensor(next_obs, dtype=torch.float, device=self.device)
        terminated = torch.as_tensor(terminated, dtype=torch.float, device=self.device).reshape(-1, 1)

        q_value = self.policy_net(obs).gather(1, action)
        with torch.no_grad():
            next_q_values = self.target_net(next_obs).max(dim=1).values.detach().reshape(-1, 1)
            expected_q_values = reward + self.gamma * next_q_values * (1 - terminated)

        loss = F.smooth_l1_loss(q_value, expected_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), max_norm=self.max_grad_norm)
        self.optimizer.step()

        return loss.item()