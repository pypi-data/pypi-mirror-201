import gymnasium as gym
import numpy as np

from ..agents.agent import Agent


def evaluate(model: Agent, env: gym.Env, num_episodes: int = 10):
    episode_rewards = []

    for _ in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0
        terminated = False
        while not terminated:
            action = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward

        episode_rewards.append(episode_reward)
        env.close()

    return np.mean(episode_rewards), np.std(episode_rewards)
