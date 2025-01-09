import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Font for score and levels
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

def draw_bricks(bricks):
    """ Draw the bricks on the screen. """
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

def draw_paddle(paddle_x):
    """ Draw the paddle on the screen. """
    paddle_rect = pygame.Rect(paddle_x, SCREEN_HEIGHT - 50, 100, 10)
    pygame.draw.rect(screen, BLUE, paddle_rect)

def draw_ball(ball_x, ball_y):
    """ Draw the ball on the screen. """
    pygame.draw.circle(screen, RED, (ball_x, ball_y), 8)

def draw_score(score):
    """ Display the current score on the screen. """
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def render_game_state(bricks, paddle_x, ball_x, ball_y, score):
    """ Render the entire game state. """
    # Clear the screen
    screen.fill(BLACK)

    # Draw all game elements
    draw_bricks(bricks)
    draw_paddle(paddle_x)
    draw_ball(ball_x, ball_y)
    draw_score(score)

    # Update the display
    pygame.display.flip()
