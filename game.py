import pygame
import sys
import time

def start_game():
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
    GREEN = (255, 0, 230)

    # Font for score and levels
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)

    # Game states
    game_state = "menu"  # "menu", "game", or "level_complete"

    # Paddle properties
    PADDLE_WIDTH = 100
    PADDLE_HEIGHT = 10
    PADDLE_SPEED = 8

    # Ball properties
    BALL_RADIUS = 8

    # Brick properties
    BRICK_WIDTH = 75
    BRICK_HEIGHT = 20
    BRICK_SPACING = 10

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Variables for game levels
    current_level = 1
    max_levels = 5

    # Function to create bricks for the current level
    def create_bricks(level):
        bricks = []
        rows = 3 + level  # Increase rows as the level increases
        columns = 8
        for row in range(rows):
            for col in range(columns):
                brick_x = col * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING
                brick_y = row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_SPACING
                brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
                bricks.append(brick)
        return bricks

    # Function to reset game variables for a new level
    def reset_game(level):
        global paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy, brick_list, score
        score = 0
        paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        paddle_y = SCREEN_HEIGHT - 50
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_dx = 4 + level  # Increase ball speed with levels
        ball_dy = -4 - level
        brick_list = create_bricks(level)

    # Initialize game variables
    score = 0
    reset_game(current_level)

    # Main loop
    while True:
        global ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y, brick_list
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return score
        # Handle menu state
        if game_state == "menu":
            # Draw menu
            screen.fill(BLACK)
            title_text = font.render("Brick Breaker", True, WHITE)
            start_text = small_font.render("Press ENTER to Start", True, WHITE)
            quit_text = small_font.render("Press Q to Quit", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
            screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 350))
            pygame.display.flip()

            # Menu controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # Enter key to start
                game_state = "game"
            if keys[pygame.K_q]:  # Q key to quit
                pygame.quit()
                return score

        # Handle game state
        elif game_state == "game":
            # Key controls for the paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle_x > 0:
                paddle_x -= PADDLE_SPEED
            if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
                paddle_x += PADDLE_SPEED
            if keys[pygame.K_ESCAPE]:  # Escape key to return to menu
                game_state = "menu"
                current_level = 1
                reset_game(current_level)
                score = 0

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
                    score += 10  # Increment score by 10 points
                    break

            # Check if all bricks are destroyed
            if not brick_list:
                if current_level < max_levels:
                    current_level += 1
                    game_state = "level_complete"
                else:
                    print("You Won!")
                    pygame.quit()
                    return score
                
            # Ball falls below the paddle
            if ball_y > SCREEN_HEIGHT:
                game_state = "menu"
                current_level = 1
                return(score)

            # Clear screen
            screen.fill(BLACK)

            # Draw paddle
            pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

            # Draw ball
            pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

            # Draw bricks
            for brick in brick_list:
                pygame.draw.rect(screen, GREEN, brick)

            # Render and display the score and level
            score_text = small_font.render(f"Score: {score}", True, WHITE)
            level_text = small_font.render(f"Level: {current_level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        # Handle level complete state
        elif game_state == "level_complete":
            screen.fill(BLACK)
            level_complete_text = font.render(f"Level {current_level - 1} Complete!", True, WHITE)
            next_level_text = small_font.render("Press ENTER to Continue", True, WHITE)
            screen.blit(level_complete_text, (SCREEN_WIDTH // 2 - level_complete_text.get_width() // 2, 250))
            screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2, 350))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # Enter to continue
                game_state = "game"
                reset_game(current_level)