import pygame
import sys
from game import render_game_state
from env import BrickBreakerEnv
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False

    def draw(self, screen):
        # Draw slider background
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        
        # Calculate slider button position
        button_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        pygame.draw.rect(screen, BLUE, (button_x - 5, self.y - 5, 10, self.height + 10))
        
        # Draw label and value
        font = pygame.font.Font(None, 24)
        label_text = font.render(f"{self.label}: {self.value:.2f}", True, WHITE)
        screen.blit(label_text, (self.x, self.y - 20))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
            if abs(mouse_x - button_x) < 10 and abs(mouse_y - (self.y + self.height/2)) < 10:
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            rel_x = min(max(mouse_x - self.x, 0), self.width)
            self.value = self.min_val + (rel_x / self.width) * (self.max_val - self.min_val)

def draw_tile(screen, x, y, width, height, color, text=None, text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    if text:
        font = pygame.font.Font(None, 36)  # Default font, size 36
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)



# def draw_graph(screen, img, x, y):
#     screen.blit(img, (x, y))

# def create_plot(att_vals):
#     width, height = 600, 375
#     dpi = 300

#     # Create figure without using plt
#     fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

#     x_vals = list(att_vals.keys())
#     y_vals = list(att_vals.values())

#     ax.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label="Data Points")
#     ax.set_xlabel("Attempt Num")
#     ax.set_ylabel("Score")
#     ax.legend()
#     ax.grid(True)

#     # Use FigureCanvasAgg to save the figure without interfering with Pygame
#     canvas = FigureCanvas(fig)
#     canvas.draw()
    
#     fig.savefig("New/plot.png", dpi=dpi, bbox_inches='tight')  # Save figure

#     plt.close(fig)

pygame.init()
clock = pygame.time.Clock()

sliders = [
    Slider(150, 425, 200, 10, -100, 100, 25, "Brick Hit Reward"),
    Slider(150, 475, 200, 10, -100, 100, 15, "Paddle Hit Reward"),
    Slider(150, 525, 200, 10, -100, 100, -50, "Loss Penalty"),
    Slider(150, 575, 200, 10, -100, 100, 0, "Time Alive Reward")
]

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

def dash(screen, env, action):
    global attempt_num, attempt_vals, max_val
    # create_plot(attempt_vals)
    screen.fill(BLACK)
    
    # Define tiles
    tile_width = 2
    tile_height = 750
    start_x = SCREEN_WIDTH // 2 - tile_width // 2
    start_y = 0

    # Draw tiles
    draw_tile(screen, start_x, start_y, tile_width, tile_height, WHITE)


    tile_width = 600
    tile_height = 2
    start_x = 0
    start_y = SCREEN_HEIGHT // 2 - tile_height // 2

    draw_tile(screen, start_x, start_y, tile_width, tile_height, WHITE)

    # start_x = 0
    # start_y = 375
    # plot_img = pygame.image.load("New/plot.png")
    # img_width = 600
    # img_height = 375
    # resized_img = pygame.transform.scale(plot_img, (img_width, img_height))

    for slider in sliders:
        slider.draw(screen)
    
    # Update reward values in env
    env.brick_reward = sliders[0].value
    env.paddle_reward = sliders[1].value
    env.loss_penalty = sliders[2].value
    env.time_reward = sliders[3].value
    

    start_x = 0
    start_y = 0
    tile_width = 600
    tile_height = 375

    draw_tile(screen, start_x, start_y, tile_width, tile_height, BLACK, f'Best score: {max_val[0]} - Attempt Number: {max_val[1]}', WHITE)
    
    next_state, reward, score, done, _ = env.step(action)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        # Handle slider events
        for slider in sliders:
            slider.handle_event(event)
    
    if env.ball_y > env.GAME_HEIGHT:
        attempt_vals[attempt_num] = score
        if score > max_val[0]:
            max_val = [score, attempt_num]
        attempt_num += 1
        # create_plot(attempt_vals)
        env.reset()


    # Flip the screen
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    
    return next_state, reward, done