import pygame
import numpy as np
from env import BrickBreakerEnv
from game import render_overlay

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 2560  # Total width including overlay sections
SCREEN_HEIGHT = 1600  # Keep height same as game view

# Create the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agent Visualization")

# Fonts
font = pygame.font.Font(None, 36)

# Initialize the environment
env = BrickBreakerEnv()

# Create surfaces for overlay
game_surface = pygame.Surface((800, 600))  # Game view (agent's perspective)
graph_surface = pygame.Surface((400, 300))  # Graph section
info_surface = pygame.Surface((400, 300))  # Info section
while True:
    render_overlay(game_surface, graph_surface, info_surface, game_state=None)