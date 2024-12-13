import pygame
import sys

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

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 5
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 50

# Ball properties
BALL_RADIUS = 8
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 4
ball_dy = -4

# Brick properties
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_SPACING = 10
brick_list = []

# Create bricks
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick_x = col * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING
        brick_y = row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_SPACING
        brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
        brick_list.append(brick)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key controls for the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and paddle_x > 0:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_d] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x += PADDLE_SPEED

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= SCREEN_WIDTH:
        ball_dx = -ball_dx
    if ball_y - BALL_RADIUS <= 0:
        ball_dy = -ball_dy

    # Ball collision with paddle
    if (
        paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT
        and paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH
    ):
        ball_dy = -ball_dy

    # Ball collision with bricks
    for brick in brick_list[:]:
        if brick.collidepoint(ball_x, ball_y):
            brick_list.remove(brick)
            ball_dy = -ball_dy
            break

    # Ball falls below the paddle
    if ball_y > SCREEN_HEIGHT:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Clear screen
    screen.fill(BLACK)

    # Draw paddle
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

    # Draw bricks
    for brick in brick_list:
        pygame.draw.rect(screen, GREEN, brick)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
