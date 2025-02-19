import pygame
import sys
from dashboard import dash
from env import BrickEnvironment  # Adjust import based on your env file name
from agent import DQNAgent  # Adjust import based on your agent file name

def test_dash():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Adjust size as needed
    pygame.display.set_caption("AI Training Visualization Test")

    # Initialize environment and agent
    brick_env = BrickEnvironment()
    agent = DQNAgent(state_size=brick_env.state_size, 
                    action_size=brick_env.action_size)  # Adjust parameters as needed

    # Test loop
    running = True
    state = brick_env.reset()
    
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get action from agent
        action = agent.choose_action(state)
        
        try:
            # Update dashboard
            dash(screen, brick_env, action)
            pygame.display.flip()
        except Exception as e:
            print(f"Error in dashboard: {e}")
            running = False
        
        # Update environment
        next_state, reward, done, _ = brick_env.step(action)
        state = next_state if not done else brick_env.reset()
        
        # Optional: Add delay to make visualization visible
        pygame.time.delay(10)  # 10ms delay, adjust as needed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    test_dash() 