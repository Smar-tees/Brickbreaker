import pygame

pygame.init()


WIDTH = 600
HEIGHT = 750

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)

# Font for score and levels
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

def draw_bricks(screen, bricks):
    for brick in bricks:
        pygame.draw.rect(screen, PURPLE, brick)

def draw_ball(screen, ball_x, ball_y):
    pygame.draw.circle(screen, RED, (ball_x, ball_y), 8)

def draw_paddle(screen, paddle_x, paddle_y):
    paddle_rect = pygame.Rect(paddle_x, paddle_y, 100, 10)
    pygame.draw.rect(screen, BLUE, paddle_rect)

def draw_text(screen, score, attempt_num, score_x, attempt_x):
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    attempt_text = small_font.render(f"Attempt: {attempt_num}", True, WHITE)
    screen.blit(score_text, (score_x, 10))
    screen.blit(attempt_text, (attempt_x, 10))

def render_game_state(screen, bricks, paddle_x, paddle_y, ball_x, ball_y, score_x, score, attempt_num, attempt_x):
    draw_bricks(screen, bricks)
    draw_paddle(screen, paddle_x, paddle_y)
    draw_ball(screen, ball_x, ball_y)
    draw_text(screen, score, attempt_num, score_x, attempt_x)

    # Update the display
    pygame.display.flip()