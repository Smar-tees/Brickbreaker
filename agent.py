import pyautogui
import numpy as np
import pygame
import game
from env import BrickBreakerEnv

class Agent:
    def __init__(self, env):
        self.env = env
        self.clock = pygame.time.Clock()  # Clock to cap the tick rate

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
            # Process agent's action
            action = self.rule_based_policy(state)
            state, reward, done, _ = self.env.step(action)
            total_reward += reward

            # Render the updated game state
            game.render_game_state(self.env.bricks, self.env.paddle_x, self.env.ball_x, self.env.ball_y, self.env.score)

            # Cap the frame rate to 60 FPS
            self.clock.tick(120)

            # Print state and action for debugging
            # print(f"State: {state}, Action: {action}, Reward: {reward}")

        # print(f"Total Reward: {total_reward}")

# Initialize the environment
env = BrickBreakerEnv()

# Create the agent and play the game
agent = Agent(env)
agent.play_game()
