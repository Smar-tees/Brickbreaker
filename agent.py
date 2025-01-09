import pyautogui
import numpy as np
from env import BrickBreakerEnv
import pygame

class Agent:
    def __init__(self, env):
        self.env = env
        self.clock = pygame.time.Clock()

    def rule_based_policy(self, state):
        """
        Simple rule-based policy:
        - If the ball is to the left of the paddle, move left.
        - If the ball is to the right of the paddle, move right.
        - Otherwise, stay.
        """
        paddle_x, ball_x, ball_y, ball_dx, ball_dy, _ = state

        if ball_x < paddle_x:
            return 1  # Move left
        elif ball_x > paddle_x + 100:
            return 2  # Move right
        else:
            return 0  # Stay

    def play_game(self):
        state = self.env.reset()
        done = False
        total_reward = 0

        while not done:
            action = self.rule_based_policy(state)
            state, reward, done, _ = self.env.step(action)
            total_reward += reward

            # Print state and action for debugging
            print(f"State: {state}, Action: {action}, Reward: {reward}")

            self.clock.tick(60)

        print(f"Total Reward: {total_reward}")

# Initialize the environment
env = BrickBreakerEnv()

# Create the agent and play the game
agent = Agent(env)
agent.play_game()
