import pygame
import numpy as np
from gym import spaces
import gym
import game

class BrickBreakerEnv(gym.Env):
    def __init__(self, screen):
        super(BrickBreakerEnv, self).__init__()
        
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 750
        
        # Observations: paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks_remaining
        self.observation_space = spaces.Box(
            low=np.array([600, 600, 0, -10, -10, 0]),
            high=np.array([1200, 1200, 750, 10, 10, 100]),
            dtype=np.float32,
        )

        self.brick_start_x = self.GAME_WIDTH + 2
        self.bricks = []
        self.paddle_x = (self.GAME_WIDTH - 100) // 2 + self.GAME_WIDTH
        self.ball_x = self.GAME_WIDTH // 2 + self.GAME_WIDTH
        self.ball_y = self.GAME_HEIGHT // 2
        self.score = 0
        self.ball_dx = 4
        self.ball_dy = -4
        self.screen = screen
        self.attempt_num = 1
        self.start_time = pygame.time.get_ticks()

        self.brick_reward = 25
        self.paddle_reward = 15
        self.loss_penalty = -50
        self.time_reward = 1

        self.distance_penalty_factor = 1


        self.create_bricks()
    
    def calculate_distance_penalty(self):
        # Calculate absolute distance between paddle and ball
        distance = abs(self.paddle_x - self.ball_x)
        # Convert distance to a penalty
        penalty = distance * self.distance_penalty_factor
        return -penalty
        

    def create_bricks(self):
        rows = 5
        columns = 10
        brick_width = (self.brick_start_x // columns) - 5
        brick_height = 20
        spacing = 5

        for row in range(rows):
            for col in range(columns):
                brick_x = self.brick_start_x + (col * (brick_width + spacing))
                brick_y = row * (brick_height + spacing)
                brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                self.bricks.append(brick)
        
    def get_bricks(self):
        return self.bricks
    
    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.bricks = []
        self.paddle_x = (self.GAME_WIDTH - 100) // 2 + 600
        self.ball_x = self.GAME_WIDTH // 2 + 600
        self.ball_y = self.GAME_HEIGHT // 2
        self.ball_dx = 4
        self.ball_dy = -4
        self.score = 0
        self.attempt_num += 1
        self.create_bricks()

        # Return the initial state
        return np.array([
            self.paddle_x,
            self.ball_x,
            self.ball_y,
            self.ball_dx,
            self.ball_dy,
            len(self.bricks)
        ], dtype=np.float32)
    
    def step(self, action):
        reward = 0
        # Update paddle position based on action
        if action == 1 and self.paddle_x > self.GAME_WIDTH + 2:  # Move left
            self.paddle_x -= 8
        elif action == 2 and self.paddle_x < self.GAME_WIDTH * 2 - 100:  # Move right
            self.paddle_x += 8

        # Calculate the new ball position
        next_ball_x = self.ball_x + self.ball_dx
        next_ball_y = self.ball_y + self.ball_dy

        # Check for collision with walls
        if next_ball_x <= self.GAME_WIDTH + 2 or next_ball_x >= self.GAME_WIDTH * 2:
            self.ball_dx = -self.ball_dx
        if next_ball_y <= 0:
            self.ball_dy = -self.ball_dy

        # Check for collision with paddle
        if next_ball_y >= self.GAME_HEIGHT - 50 and self.paddle_x <= next_ball_x <= self.paddle_x + 100:
            self.ball_dy = -self.ball_dy
            reward += self.paddle_reward

        # Perform swept collision detection with bricks
        ball_rect = pygame.Rect(next_ball_x - 8, next_ball_y - 8, 16, 16)
        collided_brick = None
        for brick in self.bricks[:]:
            if ball_rect.colliderect(brick):
                collided_brick = brick
                break

        # Handle brick collision
        if collided_brick:
            self.bricks.remove(collided_brick)
            self.ball_dy = -self.ball_dy
            self.score += 10
            reward += self.brick_reward

        # Update the ball's position
        self.ball_x = next_ball_x
        self.ball_y = next_ball_y

        # current_time = pygame.time.get_ticks()
        # time_alive = (current_time - self.start_time) / 1000.0  # Convert to seconds
        # reward += self.time_reward * (time_alive / 10)

        if self.ball_y > self.GAME_HEIGHT:
            done = True
            reward += self.calculate_distance_penalty()
        
        else:
            done = False

        # Calculate observation
        state = (
            self.paddle_x,
            self.ball_x,
            self.ball_y,
            self.ball_dx,
            self.ball_dy,
            len(self.bricks))

        # Render the game state
        game.render_game_state(self.screen, self.bricks, self.paddle_x, self.GAME_HEIGHT - 50, self.ball_x, self.ball_y, self.GAME_WIDTH + 12, self.score, self.attempt_num, self.GAME_WIDTH*2 - 135)
             

        return state, reward, self.score, done, {}