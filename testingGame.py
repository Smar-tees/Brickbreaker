import pygame
import game  # Import rendering functions
from time import sleep
from env import BrickBreakerEnv

# Initialize Pygame
pygame.init()

# Initialize the environment
env = BrickBreakerEnv()

# Create a clock to control frame rate
clock = pygame.time.Clock()

def show_menu():
    """ Display the Game Over screen and wait for player input to restart or quit. """
    screen = pygame.display.set_mode((env.SCREEN_WIDTH, env.SCREEN_HEIGHT))
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Menu", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    # Display the texts
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (env.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(restart_text, (env.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
    screen.blit(quit_text, (env.SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))
    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                waiting = False
                return "restart"
            elif keys[pygame.K_q]:
                pygame.quit()
                exit()

# Main game loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Capture user input for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        env.step(1)  # Move left
    elif keys[pygame.K_RIGHT]:
        env.step(2)  # Move right
    else:
        env.step(0)  # Stay

    # Render the game state
    game.render_game_state(env.bricks, env.paddle_x, env.ball_x, env.ball_y, env.score)

    # Check if the ball has fallen below the paddle (Game Over condition)
    if env.ball_y > env.SCREEN_HEIGHT:
        result = show_menu()
        if result == "restart":
            env = BrickBreakerEnv()  # Reset the environment
    
    if keys[pygame.K_ESCAPE]:
        result = show_menu()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
