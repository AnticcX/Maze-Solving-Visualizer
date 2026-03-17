import pygame, sys

from core.maze import Maze
from core.event_handler import EventHandler
from ui.renderer import MazeRenderer
from config import ScreenSize, MazeSize
from ui.buttons import Buttons

"""
Main entry point for the Maze Solver application.
Initializes the Pygame environment, creates the main window, and sets up the maze, renderer, and event handler.
"""
def main():
    pygame.display.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((ScreenSize.width, ScreenSize.height))
    pygame.display.set_caption("Maze Generator & Solver")
    pygame.display.flip()
    clock = pygame.time.Clock()
    
    maze = Maze()
    maze.generate_random(MazeSize.width, MazeSize.height, (1, 1), (MazeSize.width-3, MazeSize.height-3), 0.025)
    maze.solve()
    
    renderer = MazeRenderer(screen, clock)
    renderer.reset_screen()
    
    event_handler = EventHandler(maze, renderer)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            Buttons.rows_input_box.handle_event(event)
            Buttons.columns_input_box.handle_event(event)
            Buttons.speed_input_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                event_handler.handle_button_click(event.pos)
            
        
        if maze.grid != renderer.cached_grid:
            renderer.draw_static_maze(maze)
        renderer.render(maze)
        
        clock.tick(255)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
