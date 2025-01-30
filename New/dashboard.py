import pygame
import sys
from game import render_game_state
from env import BrickBreakerEnv
from time import sleep

def draw_tile(screen, x, y, width, height, color, text=None, text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    if text:
        font = pygame.font.Font(None, 36)  # Default font, size 36
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

def draw_graph(screen, img, x, y):
    screen.blit(img, (x, y))

def draw_game(screen, x, y):
    paddle_x = (SCREEN_WIDTH // 2 - 100) // 2 + x
    paddle_y = SCREEN_HEIGHT - 50
    ball_x = SCREEN_WIDTH // 4 + x
    ball_y = SCREEN_HEIGHT // 4 + y
    score = 0
    score_x = x + 12
    attempt_x = SCREEN_WIDTH - 135
    render_game_state(screen, env.get_bricks(), paddle_x, paddle_y, ball_x, ball_y, score_x, score, attempt_num, attempt_x)

def get_attempt_num():
    return attempt_num

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")
env = BrickBreakerEnv(screen)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (255, 0, 255)

while True:
    screen.fill(BLACK)
    attempt_num = 1
    attempt_vals = {0, 0}
    
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

    start_x = 0
    start_y = 375
    plot_img = pygame.image.load("New/temp_plot.png")
    img_width = 600
    img_height = 375
    resized_img = pygame.transform.scale(plot_img, (img_width, img_height))

    draw_graph(screen, resized_img, start_x, start_y)

    start_x = 0
    start_y = 0
    tile_width = 600
    tile_height = 375

    for key, val in 

    draw_tile(screen, start_x, start_y, tile_width, tile_height, BLACK, 'Best score: 10 - Attempt Number: 1', WHITE)
    
    # Capture user input for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        score = env.step(1)  # Move left
    elif keys[pygame.K_RIGHT]:
        score = env.step(2)  # Move right
    else:
        score = env.step(0)  # Stay
    
    if env.ball_y > env.GAME_HEIGHT:
        attempt_vals[attempt_num] = score
        attempt_num += 1
        env.reset()


    # Flip the screen
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    
    clock.tick(60)