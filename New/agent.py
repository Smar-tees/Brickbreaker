import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from net import DQN


class Agent:
    def __init__(self, state_size, action_size, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.2, epsilon_decay=0.95):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration-exploitation tradeoff
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        # Initialize the Q-network
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()  # Mean Squared Error loss for Q-learning

        # Replay memory (experience replay)
        self.memory = []
        self.batch_size = 64
        self.memory_size = 10000

    def choose_action(self, state):
        """ Epsilon-greedy action selection """
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)  # Random action
        state = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.model(state)
        print(torch.argmax(q_values).item())
        return torch.argmax(q_values).item()  # Choose action with highest Q-value

    def remember(self, state, action, reward, next_state, done):
        """ Store experiences in memory """
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)  # Remove the oldest experience
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        """ Train the network using replay memory """
        if len(self.memory) < self.batch_size:
            return

        # Sample random batch from memory
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.BoolTensor(dones)

        # Compute current Q-values
        current_q = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        # Compute target Q-values
        next_q = self.model(next_states).max(1)[0].detach()  # Detach to stop gradient flow
        target_q = rewards + (self.gamma * next_q * ~dones)

        # Compute loss
        loss = self.criterion(current_q, target_q)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Reduce exploration (epsilon decay)
    
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


