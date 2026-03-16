import pygame, sys

from core.maze import Maze
from ui.renderer import MazeRenderer

def main():
    pygame.display.init()
    pygame.font.init()
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Generator & Solver")
    pygame.display.flip()
    clock = pygame.time.Clock()
    
    maze = Maze(screen, clock)
    maze.generate_random(100, 100, (1, 1), (47, 47))
    maze.solve()
    
    renderer = MazeRenderer(screen, clock)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if maze.grid != renderer.cached_grid:
            renderer.draw_static_maze(maze)
        renderer.render(maze)
        
        clock.tick(60)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()