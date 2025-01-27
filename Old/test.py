import matplotlib.pyplot as plt
import numpy as np
import pygame

# Create some data
x = np.arange(0, 10, 0.1)
y = np.sin(x)

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the data
ax.plot(x, y)

# Save the figure to a temporary file
plt.savefig("temp_plot.png")



# Initialize Pygame
pygame.init()

# Load the image
plot_img = pygame.image.load("temp_plot.png")

# Get the dimensions of the image
img_width, img_height = plot_img.get_size()

# Create the Pygame window
screen = pygame.display.set_mode((img_width, img_height))

# Display the image
screen.blit(plot_img, (0, 0))
pygame.display.flip()

# Keep the window open until the user closes it
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()