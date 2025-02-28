import pygame
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

def draw_tile(screen, x, y, width, height, color, text=None, text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    if text:
        font = pygame.font.Font(None, 36)  # Default font, size 36
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

def create_fitness_graph(generations, avg_fitness):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(generations, avg_fitness, 'b-')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Average Fitness')
    ax.set_title('Training Progress')
    ax.grid(True)
    
    # Convert matplotlib figure to pygame surface
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()
    size = canvas.get_width_height()
    
    # Create pygame surface
    surf = pygame.image.fromstring(raw_data, size, "ARGB")
    plt.close(fig)
    
    return surf

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
attempt_num = 1
attempt_vals = {0: 0}
max_val = [0, 0]


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (255, 0, 255)

def dash(screen, average_fitness_history, best_agents_history):
    screen.fill((0, 0, 0))  # Black background
    
    # Display top 100 agents in the top half
    if best_agents_history:
        font = pygame.font.Font(None, 24)
        y_offset = 10
        x_offset = 10
        agents_per_column = 20
        column_width = 230
        
        for i, (agent_name, fitness, generation) in enumerate(best_agents_history):
            # Calculate position for multiple columns
            column = i // agents_per_column
            row = i % agents_per_column
            
            text = f"{i+1}. {agent_name} - Fitness: {fitness:.2f}"
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (x_offset + column * column_width, y_offset + row * 25))
    
    # Display fitness graph in bottom half
    # if average_fitness_history:
    #     graph_height = 300
    #     graph_width = min(len(average_fitness_history) * 2, SCREEN_WIDTH - 50)
        
    #     # Scale the values to fit the graph
    #     max_fitness = max(average_fitness_history)
    #     scaled_values = [400 + graph_height - (val / max_fitness * graph_height) for val in average_fitness_history]
        
    #     # Draw the line graph
    #     points = [(i * 2 + 25, val) for i, val in enumerate(scaled_values)]
    #     if len(points) > 1:
    #         pygame.draw.lines(screen, (0, 255, 0), False, points, 2)
    
    pygame.display.flip()