import pyautogui
import game
import numpy as np
import random

class Agent:
    def __init__(self):
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        self.q_table = {}

    def get_action(self, state):
        # Epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1, 2])  # Random action
        else:
            return np.argmax(self.q_table.get(state, [0, 0, 0]))

    def update_epsilon(self):
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


final_score = game.start_game()

print(final_score)