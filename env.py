import pygame
import gym
import numpy as np
from gym import spaces
import game  # Import rendering functions
from time import sleep

class BrickBreakerEnv(gym.Env):
    def __init__(self):
        super(BrickBreakerEnv, self).__init__()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # Actions: 0 = stay, 1 = move left, 2 = move right
        self.action_space = spaces.Discrete(3)

        # Observations: paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks_remaining
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, -10, -10, 0]),
            high=np.array([self.SCREEN_WIDTH, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 10, 10, 100]),
            dtype=np.float32
        )

        # Game state variables
        self.paddle_x = (self.SCREEN_WIDTH - 100) // 2
        self.ball_x = self.SCREEN_WIDTH // 2
        self.ball_y = self.SCREEN_HEIGHT // 2
        self.ball_dx = 4
        self.ball_dy = -4
        self.bricks = []
        self.score = 0

        # Create bricks
        self.create_bricks()

    def create_bricks(self):
        rows = 5
        columns = 10
        brick_width = 75
        brick_height = 20
        spacing = 5

        for row in range(rows):
            for col in range(columns):
                brick_x = col * (brick_width + spacing)
                brick_y = row * (brick_height + spacing)
                brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                self.bricks.append(brick)
    
    def reset(self):
        self.paddle_x = (self.SCREEN_WIDTH - 100) // 2
        self.ball_x = self.SCREEN_WIDTH // 2
        self.ball_y = self.SCREEN_HEIGHT // 2
        self.ball_dx = 4
        self.ball_dy = -4
        self.score = 0
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
        # Update paddle position based on action
        if action == 1 and self.paddle_x > 0:  # Move left
            self.paddle_x -= 8
        elif action == 2 and self.paddle_x < self.SCREEN_WIDTH - 100:  # Move right
            self.paddle_x += 8

        # Update ball position
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Ball collision with walls
        if self.ball_x <= 0 or self.ball_x >= self.SCREEN_WIDTH:
            self.ball_dx = -self.ball_dx
        if self.ball_y <= 0:
            self.ball_dy = -self.ball_dy

        # Ball collision with paddle
        if self.ball_y >= self.SCREEN_HEIGHT - 50 and self.paddle_x <= self.ball_x <= self.paddle_x + 100:
            self.ball_dy = -self.ball_dy

        # Ball collision with bricks
        for brick in self.bricks[:]:
            if pygame.Rect(self.ball_x - 8, self.ball_y - 8, 16, 16).colliderect(brick):
                self.bricks.remove(brick)
                self.ball_dy = -self.ball_dy
                self.score += 10

        # Ball falls below paddle
        if self.ball_y > self.SCREEN_HEIGHT:
            done = True
            reward = -100
        else:
            done = False
            reward = 0

        # Calculate observation
        state = np.array([
            self.paddle_x,
            self.ball_x,
            self.ball_y,
            self.ball_dx,
            self.ball_dy,
            len(self.bricks)
        ], dtype=np.float32)

        # Render the game state
        game.render_game_state(self.bricks, self.paddle_x, self.ball_x, self.ball_y, self.score)

        return state, reward, done, {}

