import pygame
from pygame import Surface, sprite, display, Rect
from typing import Optional, Union

from components import Wall, Exit, Runner, Path, GhostPath
from ui.fps_counter import FPSCounter
from algorithms import Grid
from core.maze import Maze
from core.Types import RGB
from ui.buttons import Buttons
from config import (
    MAZE_BACKGROUND_COLOR, TITLE_FONT, BUTTON_FONT, LABEL_FONT, STATS_FONT,
    BUTTON_TEXT_COLOR, DEFAULT_BUTTON_COLOR, NO_PATH_TEXT_COLOR, DFS_TEXT_COLOR, BFS_TEXT_COLOR,
    SELECTED_BFS_COLOR, SELECTED_DFS_COLOR, UNSELECTED_BFS_COLOR, UNSELECTED_DFS_COLOR,
    STATS_START_Y_POS, STATS_LABEL_GAP,
    DisplayOffset, Panel, Tile, Speed
)

""" 
Maze Renderer for the Maze Solver application.
This module defines the MazeRenderer class, which is responsible for rendering the maze and its components on the screen.
The MazeRenderer class handles drawing the maze, updating the left panel with algorithm information, and animating the pathfinding process.
"""
class MazeRenderer:
    def __init__(self, screen: Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.all_sprites = sprite.RenderUpdates()
        self.background = Surface(screen.get_size())
        self.background.fill(MAZE_BACKGROUND_COLOR)
        self.clean_background = self.background.copy()
        
        self.all_sprites.add(FPSCounter(0, 0, self.clock))
        
        self.cached_grid: Grid = None
        self.region_update_queue = []
        
        self.historical_trail_index = -1
        self.trail_index = -1
        self.simulation_running = False
    
    def _draw_button(
        self, 
        panel: Surface,
        button_rect: Rect, 
        text: str, 
        font: pygame.font.Font, 
        button_color: Optional[RGB] = DEFAULT_BUTTON_COLOR, 
        text_color: Optional[RGB] = BUTTON_TEXT_COLOR
        ) -> None:
        """Draw a button on the given panel with specified properties.

        Args: 
            panel (Surface): The Pygame surface to draw the button on.
            button_rect (Rect): The rectangle defining the button's position and size.
            text (str): The text to display on the button.
            font (pygame.font.Font): The font to use for rendering the button text.
            button_color (Optional[RGB], optional): The background color of the button. Defaults to DEFAULT_BUTTON_COLOR.
            text_color (Optional[RGB], optional): The color of the button text. Defaults to BUTTON_TEXT_COLOR.
        """
        button = pygame.Surface((button_rect.width, button_rect.height))
        button.fill(button_color)
        
        label = font.render(text, True, text_color)
        label_rect = label.get_rect(center=(button_rect.width // 2, button_rect.height // 2))
        button.blit(label, label_rect)
        panel.blit(button, button_rect.topleft)

    def _draw_left_panel(self, maze: Maze) -> None:
        """Draw the left panel with algorithm information and buttons.

        Args:
            maze (Maze): The Maze object containing the current state of the maze and algorithm information.
        """
        panel = pygame.Surface((Panel.width, Panel.height))
        panel.fill((20, 20, 20))
        title = TITLE_FONT.render("Maze Solver", True, (255, 255, 255))
        
        panel.blit(title, (60, 25))
        Buttons.rows_input_box.draw(panel, LABEL_FONT)
        panel.blit(LABEL_FONT.render("Rows:", True, (255, 255, 255)), (110, 68))
        Buttons.rows_input_box.draw(panel, LABEL_FONT)
        panel.blit(LABEL_FONT.render("Columns:", True, (255, 255, 255)), (92, 158))
        Buttons.columns_input_box.draw(panel, LABEL_FONT)
        panel.blit(LABEL_FONT.render("Simulation Speed:", True, (255, 255, 255)), (30, 248))
        Buttons.speed_input_box.draw(panel, LABEL_FONT)
        
        self._draw_button(panel, Buttons.bfs, 'BFS', BUTTON_FONT, SELECTED_BFS_COLOR if maze.selected_algorithm.lower() == 'bfs' else UNSELECTED_BFS_COLOR, BFS_TEXT_COLOR)
        self._draw_button(panel, Buttons.dfs, 'DFS', BUTTON_FONT, SELECTED_DFS_COLOR if maze.selected_algorithm.lower() == 'dfs' else UNSELECTED_DFS_COLOR, DFS_TEXT_COLOR)
        self._draw_button(panel, Buttons.generate, 'Generate Maze', BUTTON_FONT)
        self._draw_button(panel, Buttons.solve, 'Solve', BUTTON_FONT)
        self._draw_button(panel, Buttons.reset, 'Reset', BUTTON_FONT)
        self._draw_button(panel, Buttons.no_path, 'No Path Test', BUTTON_FONT, text_color=NO_PATH_TEXT_COLOR)
        
        algo = maze.selected_algorithm if maze.selected_algorithm else "None"
        path_len = len(maze.path) if maze.path else 0
        visited = maze.visited_count if maze.visited_count else 0
        runtime = maze.runtime if maze.runtime else 0.0

        # Status text
        if maze.selected_algorithm is None:
            status = "Idle"
        elif maze.path:
            status = "Path Found"
        else:
            status = "No Path Found"

        # Status color
        if status == "Path Found":
            status_color = (0, 255, 0)
        elif status == "No Path Found":
            status_color = (255, 80, 80)
        else:
            status_color = (255, 255, 255)
            
        panel.blit(STATS_FONT.render(f"Algorithm: {algo}", True, (255, 255, 255)), (25, STATS_START_Y_POS))
        panel.blit(STATS_FONT.render(f"Path Length: {path_len}", True, (255, 255, 255)), (25, STATS_START_Y_POS + STATS_LABEL_GAP))
        panel.blit(STATS_FONT.render(f"Visited Nodes: {visited}", True, (255, 255, 255)), (25, STATS_START_Y_POS + STATS_LABEL_GAP * 2))
        panel.blit(STATS_FONT.render(f"Runtime: {runtime:.6f}s", True, (255, 255, 255)), (25, STATS_START_Y_POS + STATS_LABEL_GAP * 3))
        panel.blit(STATS_FONT.render(f"Status: {status}", True, status_color), (25, STATS_START_Y_POS + STATS_LABEL_GAP * 4))
        
        self.background.blit(panel, (0, 0))
        self.region_update_queue.append(panel.get_rect())
    
    def _center_maze(self, maze: Maze) -> None:
        """Calculate the display offset to center the maze on the screen.

        Args:
            maze (Maze): The Maze object to center.
        """
        screen_width, screen_height = self.screen.get_size()
        
        maze_pixel_width = len(maze.grid[0]) * Tile.size
        maze_pixel_height = len(maze.grid) * Tile.size
        
        available_width = screen_width - Panel.width
        available_height = screen_height - Panel.top_margin - Panel.bottom_margin
        
        DisplayOffset.x = Panel.width + max((available_width - maze_pixel_width) // 2, 0)
        DisplayOffset.y = Panel.top_margin + max((available_height - maze_pixel_height) // 2, 0)

    def _add_tile(self, x_grid: int, y_grid: int, tile: Union[Path, GhostPath]) -> None:
        """Add a tile (path or ghost path) to the maze display at the specified grid coordinates.

        Args: 
            x_grid (int): The x-coordinate in the maze grid.
            y_grid (int): The y-coordinate in the maze grid.
            tile (Union[Path, GhostPath]): The type of tile to add (either a Path or GhostPath).
        """
        x = x_grid * Tile.size + DisplayOffset.x
        y = y_grid * Tile.size + DisplayOffset.y
        path: Union[Path, GhostPath] = tile(x, y)
        self.background.blit(path.image, path.rect)
        self.region_update_queue.append(path.rect)
            
    def _walk_path(self, maze: Maze, historical: bool = True) -> None:
        """Animate the pathfinding process by walking through the path or historical trail of the maze.

        Args:
            maze (Maze): The Maze object containing the current state of the maze and algorithm information.
            historical (bool, optional): Whether to walk through the historical trail or the final path. Defaults to True.
        """
        for _ in range(Speed.current):
            y, x = maze.solve_history[self.historical_trail_index] if historical else maze.path[self.trail_index]
            if maze.grid[y][x].lower() != Tile.runner and maze.grid[y][x].lower() != Tile.exit:
                if historical:
                    self._add_tile(x, y, GhostPath)
                else:                   
                    self._add_tile(x, y, Path)
            if historical: self.historical_trail_index += 1
            else: self.trail_index += 1
            if historical and self.historical_trail_index >= len(maze.solve_history): break
            elif not historical and self.trail_index >= len(maze.path): break

    def reset_screen(self) -> None:
        """Reset the maze display to its initial state, clearing all paths and sprites while keeping the maze structure intact.
        """
        Tile.update_size()
        self.all_sprites.clear(self.screen, self.background)
        self.all_sprites.empty()
        self.all_sprites.add(FPSCounter(0, 0, self.clock))
        self.background = self.clean_background.copy()
        self.cached_grid: Grid = None
        self.region_update_queue = [self.screen.get_rect()]
        self.trail_index = -1
        self.historical_trail_index = -1
        self.simulation_running = False

    def draw_static_maze(self, maze: Maze) -> None:
        """Draw the static maze structure on the screen without any pathfinding animation.

        Args:
            maze (Maze): The Maze object containing the static maze structure.
        """
        self._center_maze(maze)
        for row_i, row in enumerate(maze.grid):
            for col_i, char in enumerate(row):
                x = col_i * Tile.size + DisplayOffset.x
                y = row_i * Tile.size + DisplayOffset.y
                
                if char == Tile.wall:
                    wall = Wall(x, y)
                    self.background.blit(wall.image, wall.rect)
                    self.region_update_queue.append(wall.rect)
                elif char.lower() == Tile.exit: 
                    self.all_sprites.add(Exit(x, y))
                elif char.lower() == Tile.runner:
                    self.all_sprites.add(Runner(x, y))
        self.cached_grid = maze.grid
        
    def render(self, maze: Maze) -> None:
        """Render the maze and its components on the screen, including the left panel, static maze structure, and pathfinding animation.

        Args:
            maze (Maze): The Maze object containing the current state of the maze and algorithm information.
        """
        self._draw_left_panel(maze)
        if self.simulation_running and self.historical_trail_index < len(maze.solve_history):
            self._walk_path(maze)
        elif self.simulation_running and len(maze.path) > 0 and self.trail_index < len(maze.path):
            self._walk_path(maze, historical=False)

        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        self.region_update_queue.extend(self.all_sprites.draw(self.screen))
        display.update(self.region_update_queue)
        self.region_update_queue = []
