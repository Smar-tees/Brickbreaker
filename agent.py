import pyautogui
import numpy as np
import pygame
import game
from env import BrickBreakerEnv
import random
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, env):
        self.env = env
        self.q_table = {}  # Q-value table
        self.epsilon = 1.0  # Initial exploration rate
        self.epsilon_min = 0.1  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay rate for epsilon
    
    def get_state(self):
        state = (
            self.env.paddle_x,
            self.env.ball_x,
            self.env.ball_y,
            self.env.ball_dx,
            self.env.ball_dy,
            len(self.env.bricks),
        )

        return state
    
    def get_q_table(self):
        table = self.q_table
        return table
    
    def choose_action(self, state):
        """ Choose an action using the epsilon-greedy policy. """
        state = tuple(state)  # Ensure the state is a tuple

        if random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            return self.env.action_space.sample()
        else:
            # Exploit: choose the action with the highest Q-value
            return np.argmax(self.q_table.get(state, [0, 0, 0]))
    
    def update_q_value(self, state, action, reward, next_state, alpha=0.1, gamma=0.99):
        # Convert next_state to a tuple
        if state not in self.q_table:
            self.q_table[state] = {0:0, 1:0, 2:0}
        
        current_q = self.q_table[state][action]

        if next_state not in self.q_table:
            self.q_table[next_state] = {0:0, 1:0, 2:0}

        max_future_q = max(self.q_table[next_state].values())

        # Q-learning formula
        new_q = current_q + alpha * (reward)
        self.q_table[state][action] = new_q
        print(self.q_table[state][action])
    
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def display_q_table(self, q_table):
        # print(q_table, '\n')
        for key, val in q_table.items():
            for key, values in val.items():
                if values != 0:
                    print(key, values)
            




        # plt.clf()  # Clear the current figure
        # plt.imshow(q_table, cmap="coolwarm", interpolation="nearest")
        # plt.colorbar()
        # plt.title("Q-Table Heatmap")
        # plt.xlabel("Actions")
        # plt.ylabel("States")
        # plt.draw()
        # plt.pause(0.1)



# Initialize the environment
env = BrickBreakerEnv()

# Create the agent and play the game
agent = Agent(env)
clock = pygame.time.Clock()

for episode in range(1000):  # Number of episodes to train
    state = agent.get_state()
    done = False
    total_reward = 0

    while not done:
        # Choose an action
        action = agent.choose_action(state)

        # Take the action in the environment
        next_state, reward, done, _ = env.step(action)

        # Update Q-value
        agent.update_q_value(state, action, reward, next_state)

        # Update state
        state = next_state
        total_reward += reward

        q_table = agent.get_q_table()

        agent.display_q_table(q_table)

        clock.tick(10)
        

    # Decay epsilon
    agent.decay_epsilon()

    print(f"Episode {episode + 1}: Total Reward: {total_reward}")

