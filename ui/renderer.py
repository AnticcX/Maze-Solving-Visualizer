import pygame
from pygame import Surface, sprite, display
from typing import Optional, Union

from config import TILE_SIZE, MAZE_BACKGROUND_COLOR, SIMULATION_SPEED, DisplayOffset, Panel
from components import Wall, Exit, Runner, Path, GhostPath
from ui.fpsCounter import FPSCounter
from algorithms import Grid
from core.maze import Maze


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
        
        self.trail_index = -1
    
    def _center_maze(self, maze: Maze) -> None:
        screen_width, screen_height = self.screen.get_size()
        
        maze_pixel_width = len(maze.grid[0]) * TILE_SIZE
        maze_pixel_height = len(maze.grid) * TILE_SIZE
        
        available_width = screen_width - Panel.width
        available_height = screen_height - Panel.top_margin - Panel.bottom_margin
        
        DisplayOffset.x = Panel.width + max((available_width - maze_pixel_width) // 2, 0)
        DisplayOffset.y = Panel.top_margin + max((available_height - maze_pixel_height) // 2, 0)

    def _add_tile(self, x_grid: int, y_grid: int, tile: Union[Path, GhostPath]) -> None:
        x = x_grid * TILE_SIZE + DisplayOffset.x
        y = y_grid * TILE_SIZE + DisplayOffset.y
        path: Union[Path, GhostPath] = tile(x, y)
        self.background.blit(path.image, path.rect)
        self.region_update_queue.append(path.rect)
            
    def _walk_path(self, maze: Maze) -> None:
        for _ in range(SIMULATION_SPEED):
            y, x = maze.solve_history[self.trail_index]
            if maze.grid[y][x] != 'S' and maze.grid[y][x] != 'E':
                if (y, x) in maze.path: self._add_tile(x, y, Path)
                else:                   self._add_tile(x, y, GhostPath)
                    
            self.trail_index += 1
            if self.trail_index >= len(maze.solve_history): break
        
    def reset_screen(self) -> None:
        self.all_sprites.clear(self.screen, self.background)
        self.all_sprites.empty()
        self.all_sprites.add(FPSCounter(0, 0, self.clock))
        self.background = self.clean_background.copy()
        self.cached_grid: Grid = None
        self.region_update_queue = [self.screen.get_rect()]
        self.trail_index = -1

    def draw_static_maze(self, maze: Maze) -> None:
        self._center_maze(maze)
        for row_i, row in enumerate(maze.grid):
            for col_i, char in enumerate(row):
                x = col_i * TILE_SIZE + DisplayOffset.x
                y = row_i * TILE_SIZE + DisplayOffset.y
                
                if char == '#':
                    wall = Wall(x, y)
                    self.background.blit(wall.image, wall.rect)
                    self.region_update_queue.append(wall.rect)
                elif char.lower() == 'e': 
                    self.all_sprites.add(Exit(x, y))
                elif char.lower() == 's':
                    self.all_sprites.add(Runner(x, y))
        self.cached_grid = maze.grid
        
    def render(self, maze: Maze) -> None:
        if self.trail_index < len(maze.solve_history):
            self._walk_path(maze)
            
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        self.region_update_queue.extend(self.all_sprites.draw(self.screen))
        display.update(self.region_update_queue)
        self.region_update_queue = []