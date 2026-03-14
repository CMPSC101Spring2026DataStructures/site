
# OBC

"""
Simple Pygame Game - Tutorial 01
A basic interactive game where you control a moving circle.

Students will copy code here following the tutorial instructions.
"""

# COMPLETED-TASK: Add imports here
import pygame

# COMPLETED-TASK: Add pygame initialization
pygame.init()

# COMPLETED-TASK: Add screen setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("My First Pygame!")

# COMPLETED-TASK: Add clock and position variables
clock = pygame.time.Clock()

# Starting position of our circle (center of screen)
x, y = 300, 200

# Game running state
running = True


# COMPLETED-TASK: Add game loop
while running:
    # Handle events (user input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get all pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 3
    if keys[pygame.K_RIGHT]:
        x += 3
    if keys[pygame.K_UP]:
        y -= 3
    if keys[pygame.K_DOWN]:
        y += 3

    # Clear screen with dark gray
    screen.fill((30, 30, 30))
    
    # Draw red circle
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 20)

    # Update the display
    pygame.display.flip()
    
    # Control frame rate (60 FPS)
    clock.tick(60)


# COMPLETED-TASK: Add pygame quit
pygame.quit()