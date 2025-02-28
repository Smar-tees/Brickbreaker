import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from net import DQN


class Agent:
    def __init__(self, state_size, action_size, name, number, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.2, epsilon_decay=0.95):
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
        self.name = str(name) + str(number)

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

class Population:
    def __init__(self, state_size, action_size, population_size=6):
        self.state_size = state_size
        self.action_size = action_size
        self.population_size = population_size
        self.agents = []
        self.generation = 0
        self.best_agent = None
        self.best_fitness = float('-inf')
        self.name_num = 0
        self.create_agents()

    def create_agents(self):
        for i in range(self.population_size):
            self.agents.append(Agent(self.state_size, self.action_size, self.name_num, str(i)))
        self.name_num += 1
    
    def evaluate_fitness(self, env, episodes_per_agent=5):
        fitness_scores = []
        
        for agent in self.agents:
            total_fitness = 0
            for _ in range(episodes_per_agent):
                state = env.reset()
                episode_reward = 0
                done = False
                
                while not done:
                    action = agent.choose_action(state)
                    next_state, reward, _, done, _ = env.step(action)
                    episode_reward += reward
                    state = next_state
                
                total_fitness += episode_reward
            
            avg_fitness = total_fitness / episodes_per_agent
            fitness_scores.append((agent, avg_fitness))
            
            if avg_fitness > self.best_fitness:
                self.best_fitness = avg_fitness
                self.best_agent = agent
        
        return sorted(fitness_scores, key=lambda x: x[1], reverse=True)
    
    def create_next_generation(self, fitness_scores):
        self.generation += 1
        new_agents = []
        
        # Always keep the best agent ever found
        new_agents.append(self.best_agent)
    
    # Create remaining agents through crossover and mutation
        for i in range(1, self.population_size):  # Start from 1 since we already added best_agent
            # Use self.best_agent as one parent more frequently
            parent1 = self.best_agent   
            parent2 = fitness_scores[0][0]  # Get the agent with the best fitness score
            child = self.crossover(parent1, parent2, i)
            self.mutate(child)
            new_agents.append(child)
        
        self.agents = new_agents
        self.name_num += 1
    
    def crossover(self, parent1, parent2, num):
        child = Agent(parent1.state_size, parent1.action_size, self.name_num, num)
        
        # Perform crossover for neural network weights
        for (name1, param1), (name2, param2) in zip(
            parent1.model.named_parameters(), 
            parent2.model.named_parameters()
        ):
            # Randomly choose weights from either parent
            mask = torch.rand_like(param1) > 0.5
            new_param = torch.where(mask, param1, param2)
            dict(child.model.named_parameters())[name1].data.copy_(new_param)
        
        return child
    
    def mutate(self, agent, mutation_rate=0.1, mutation_strength=0.1):
        with torch.no_grad():
            for param in agent.model.parameters():
                # Apply random mutations
                mutation_mask = torch.rand_like(param) < mutation_rate
                mutation = torch.randn_like(param) * mutation_strength
                param.data += torch.where(mutation_mask, mutation, torch.zeros_like(param))
