import pygame, sys, copy

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
    maze.generate_random(250, 250, (1, 1), (150, 150), 0.075)
    maze.solve('bfs')
    
    renderer = MazeRenderer(screen, clock)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_0:
                    renderer.reset_screen()
                    if maze.selected_algorithm == 'bfs':    maze.solve('dfs')
                    else:                                   maze.solve('bfs')
                    
                if event.key == pygame.K_1:
                    renderer.reset_screen()
                    maze = Maze(screen, clock)
                    maze.generate_random(250, 250, (1, 1), (150, 150), 0.075)
                    maze.solve()
        
        if maze.grid != renderer.cached_grid:
            renderer.draw_static_maze(maze)
        renderer.render(maze)
        
        clock.tick(255)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()