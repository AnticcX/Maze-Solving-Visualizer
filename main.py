import pygame

from maze import Maze

# TEMP MAIN FILE FOR QUICK TEST DEPLOYMENT. UPDATE BEFORE SUBMITTING PROJECT

# Initialization setup
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

maze = Maze(screen, clock)
# Parse the map once before the loop

maze.generate_random_maze(100, 100, (1, 1), (50-3, 50-3))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    maze.update()
    clock.tick(60)

pygame.quit()