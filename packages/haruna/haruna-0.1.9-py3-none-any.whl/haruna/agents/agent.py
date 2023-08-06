from __future__ import annotations

import os
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import List
from typing import Union

import gymnasium as gym
import numpy as np
import torch


class Agent:

    def __init__(self, env: gym.Env, initial_setup: bool = True) -> None:
        self.env = env
        self.initial_setup = initial_setup

    def learn(self, total_timesteps: int) -> None:
        raise NotImplementedError

    def predict(self, obs: np.ndarray, deterministic: bool = False) -> np.ndarray:
        raise NotImplementedError

    def save(self, f: Union[AnyStr, os.PathLike]) -> None:
        state_dict = self.state_dict()
        torch.save(state_dict, f)

    def setup(self) -> None:
        raise NotImplementedError

    @classmethod
    def load(cls, f: Union[AnyStr, os.PathLike], device: Union[str, torch.device] = 'cuda') -> Agent:
        device = torch.device(device if torch.cuda.is_available() else 'cpu')
        state_dict = torch.load(str(f), map_location=device)

        model = cls(env=None, initial_setup=False)
        model.load_state_dict(state_dict)
        # model.setup()

        return model

    def excluded_state_dict_keys(self) -> List[str]:
        """Returns a list of keys that should be excluded from the state dict."""
        return []

    def state_dict(self) -> Dict[str, Any]:
        """Returns a state dict that can be used to recreate the agent."""
        state_dict = {}

        for key, value in self.__dict__.items():
            if key not in self.excluded_state_dict_keys():
                state_dict[key] = value

        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        self.__dict__.update(state_dict)
