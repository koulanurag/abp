import gym
import numpy as np
import abp
import os
import time

from abp import QAdaptive

def run_task(config):
    config.name = "FruitCollection-v0"

    env_spec = gym.make(config.name)
    state = env_spec.reset()
    max_episode_steps = 300

    config.action_size = env_spec.action_space.n

    agent = QAdaptive(config)

    #Training Episodes
    for epoch in range(config.training_episode):
        state = env_spec.reset()
        for steps in range(max_episode_steps):
            action = agent.predict(state)
            state, reward, done, info = env_spec.step(action)

            agent.reward(reward)

            agent.actual_reward(-1)

            possible_fruit_locations = info["possible_fruit_locations"]
            collected_fruit = info["collected_fruit"]
            current_fruit_locations = info["current_fruit_locations"]


            r = None
            if collected_fruit is not None:
                r = possible_fruit_locations.index(collected_fruit)
                agent.reward(1)

            for i in range(9):
                if (r is None or r != i) and  possible_fruit_locations[i] in current_fruit_locations:
                    agent.reward(-1)

            if done or steps == (max_episode_steps - 1):
                agent.end_episode(state)
                break

    agent.disable_learning()

    #Test Episodes
    for epoch in range(config.test_episodes):
        state = env_spec.reset()
        for steps in range(max_episode_steps):
            if config.render:
                env_spec.render()
            action = agent.predict(state)
            state, reward, done, info = env_spec.step(action)
            agent.test_reward(-1)

            if done:
                agent.end_episode(state)
                break

    env_spec.close()
