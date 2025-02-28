import env
from agent import Population
import pygame
from env import BrickBreakerEnv
import torch
import csv
from dashboard import dash
import os

clock = pygame.time.Clock()
env = BrickBreakerEnv()

# Initialize environment and agent parameters
state_size = 6
action_size = 3

# Create population
population = Population(state_size, action_size, population_size=6)

best_model_path = 'Agents/best_model.pth'
if os.path.exists(best_model_path):
    best_agent = population.agents[0]  # Use first agent to load the model
    best_agent.model.load_state_dict(torch.load(best_model_path))
    # Copy the loaded model to all agents in the population
    for agent in population.agents[1:]:
        agent.model.load_state_dict(best_agent.model.state_dict())
    population.best_agent = best_agent

# Training parameters
num_generations = 100000
FRAMES_PER_ACTION = 3

# Add at the beginning of the file
average_fitness_history = []
best_agents = []
best_agents_history = []

for generation in range(num_generations):
    # Evaluate current population
    fitness_scores = population.evaluate_fitness(env)
    best_agent = fitness_scores[0][0]
    best_fitness = fitness_scores[0][1]
    
    # Store agent and its fitness score
    best_agents_history.append((best_agent.name, best_fitness, generation + 1))
    # Keep only top 100 agents sorted by fitness
    best_agents_history.sort(key=lambda x: x[1], reverse=True)
    best_agents_history = best_agents_history[:100]
    
    best_agents.append(best_agent)
    
    print(f"Generation {generation + 1}/{num_generations}")
    print(f"Best Fitness: {best_fitness}")
    average_fitness = sum(score for _, score in fitness_scores) / len(fitness_scores)
    print(f"Average Fitness: {average_fitness}")

    # Save best model
    if best_fitness >= best_agents_history[0][1]:
        torch.save(best_agent.model.state_dict(), f'Agents/best_model.pth')
    
    # Create next generation
    population.create_next_generation(fitness_scores)

    # Inside your generation loop, after calculating average_fitness
    average_fitness_history.append(average_fitness)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

while True:
    dash(screen, average_fitness_history, best_agents_history)