import env
from agent import Agent
import pygame
from env import BrickBreakerEnv
from dashboard import dash
import time
import torch


clock = pygame.time.Clock()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")
env = BrickBreakerEnv(screen)

# Initialize environment and agent parameters
state_size = 6  # [paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks_remaining]
action_size = 3  # Left, Right, Stay

# Create agent instance
agent = Agent(state_size, action_size)

# Load the trained model
agent.model.load_state_dict(torch.load('New/agent.pth'))
agent.model.eval()  # Set the model to evaluation mode


num_episodes = 100

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = dash(screen, env, action)

        # agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        # Train the model
        agent.replay()

        clock.tick(120)
    
    agent.decay_epsilon()

    print(f"Episode {episode + 1}/{num_episodes} - Score: {total_reward}, Epsilon: {agent.epsilon:.3f}")

torch.save(agent.model.state_dict(), 'model.pth')
