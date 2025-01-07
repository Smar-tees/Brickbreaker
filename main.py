import pygame
import gym
import numpy as np
from gym import spaces

class BrickBreakerEnv(gym.Env):
    def __init__(self):
        super(BrickBreakerEnv, self).__init__()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.action_space = spaces.Discrete(3)

        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(100,),  # Example size, adjust based on your representation
            dtype=np.float32
        )