import env
from agent import Agent

# Initialize environment and agent
brick_env = env.BrickBreakerEnv()
state_size = 6  # [paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks_remaining]
action_size = 3  # Left, Right, Stay

agent = Agent(state_size, action_size)

num_episodes = 1000

for episode in range(num_episodes):
    state = brick_env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.choose_action(state)
        next_state, reward, done, _ = brick_env.step(action)

        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        # Train the model
        agent.replay()

    print(f"Episode {episode + 1}/{num_episodes} - Score: {total_reward}, Epsilon: {agent.epsilon:.3f}")
