import pygame
import gym
import numpy as np
from gym import spaces
import random

class BrickBreakerEnv(gym.Env):
    def __init__(self):
        super(BrickBreakerEnv, self).__init__()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # Actions: 0 = stay, 1 = move left, 2 = move right
        self.action_space = spaces.Discrete(3)

        # Observations: paddle x, ball x, ball y, ball dx, ball dy
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, -10, -10]),
            high=np.array([self.SCREEN_WIDTH, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 10, 10]),
            dtype=np.float32
        )

        self.paddle_x = 0
        self.ball_x = 0
        self.ball_y = 0
        self.ball_dx = 0
        self.ball_dy = 0

    def step(self, action):
        # Update the game state based on the action

        # Calculate the reward for this step
        reward = self.get_reward()

        # Check if the game is over
        done = self.check_done()

        # Return the observation, reward, done, and info
        state = self.get_state()
        return state, reward, done, {}

    def get_state(self):
        return np.array([self.paddle_x, self.ball_x, self.ball_y, self.ball_dx, self.ball_dy], dtype=np.float32)  



    def get_reward(self):
        """ Reward function for the agent. """
        if self.ball_y > self.SCREEN_HEIGHT:
            # Ball falls below the paddle
            return -100
        elif self.level_completed() == 0:
            # Level completed
            return 100
        elif self.ball_hits_paddle():
            # Ball hits the paddle
            return 5
        elif self.ball_hits_brick():
            # Ball hits a brick
            return 10
        else:
            # Default reward
            return 0

    def ball_hits_paddle(self):
        # Logic to detect if the ball hits the paddle
        return (
            self.paddle_x <= self.ball_x <= self.paddle_x + 100 and
            self.ball_y >= self.SCREEN_HEIGHT - 50
        )

    def ball_hits_brick(self):
        # Logic to detect if the ball hits a brick
        return False  # Placeholder logic

    def level_completed(self):
        return False # Placeholder logic
        