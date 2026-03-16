import pygame, sys

from core.maze import Maze
from ui.renderer import MazeRenderer
from config import ScreenSize, MaxMazeSize

def main():
    pygame.display.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((ScreenSize.width, ScreenSize.height))
    pygame.display.set_caption("Maze Generator & Solver")
    pygame.display.flip()
    clock = pygame.time.Clock()
    
    maze = Maze(screen, clock)
    maze.generate_random(MaxMazeSize.width, MaxMazeSize.height, (1, 1), (MaxMazeSize.width-3, MaxMazeSize.height-3), 0.025)
    maze.solve('bfs')
    
    renderer = MazeRenderer(screen, clock)
    renderer.reset_screen()
    
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
                    maze.generate_random(MaxMazeSize.width, MaxMazeSize.height, (1, 1), (MaxMazeSize.width-3, MaxMazeSize.height-3), 0.025)
                    maze.solve()
        
        if maze.grid != renderer.cached_grid:
            renderer.draw_static_maze(maze)
        renderer.render(maze)
        
        clock.tick(255)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()