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
    maze.generate_random(50, 50, (1, 1), (47, 47), 0.3)
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
                if event.key == pygame.K_0:
                    ghost_trail = copy.copy(maze)
                    if maze.selected_algorithm == 'bfs':    maze.solve('dfs')
                    else:                                   maze.solve('bfs')
                    renderer.clear_ghost_trail(maze)
                    renderer.clear_trail(ghost_trail)
                    
                if event.key == pygame.K_1:
                    renderer.reset_screen()
                    maze = Maze(screen, clock)
                    maze.generate_random(50, 50, (1, 1), (47, 47), 0.3)
                    maze.solve()
        
        if maze.grid != renderer.cached_grid:
            renderer.draw_static_maze(maze)
        renderer.render(maze)
        
        clock.tick(60)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()