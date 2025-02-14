from agent import Agent

# Initialize environment and agent parameters
state_size = 6  # [paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks_remaining]
action_size = 3  # Left, Right, Stay

# Create agent instance
agent = Agent(state_size, action_size)

# Train the agent (you may want to add training code here)

# Save the trained model
import torch
torch.save(agent.model.state_dict(), 'New/agent.pth')

