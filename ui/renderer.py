import pygame
from pygame import Surface, sprite, display

from CONFIG import TILE_SIZE, MAZE_BACKGROUND_COLOR, DISPLAY_OFFSET
from components import Wall, Exit, Runner, Path
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
        
        self.all_sprites.add(FPSCounter(0, 0, self.clock))
        
        self.cached_grid: Grid = None
        self.region_update_queue = []
        
        self.trail_index = -1

    def _add_path_tile(self, x_grid: int, y_grid: int) -> None:
        x = x_grid * TILE_SIZE + DISPLAY_OFFSET.x
        y = y_grid * TILE_SIZE + DISPLAY_OFFSET.y
        path = Path(x, y)
        self.background.blit(path.image, path.rect)
        self.region_update_queue.append(path.rect)
        
    def _walk_path(self, maze: Maze) -> None:
        y, x = maze.path[self.trail_index]
        if maze.grid[y][x] != 'S' and maze.grid[y][x] != 'E':
            self._add_path_tile(x, y)
        self.trail_index += 1

    def draw_static_maze(self, maze: Maze) -> None:
        for row_i, row in enumerate(maze.grid):
            for col_i, char in enumerate(row):
                x = col_i * TILE_SIZE + DISPLAY_OFFSET.x
                y = row_i * TILE_SIZE + DISPLAY_OFFSET.y
                
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
        if self.trail_index < len(maze.path):
            self._walk_path(maze)
            
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        self.region_update_queue.extend(self.all_sprites.draw(self.screen))
        display.update(self.region_update_queue)
        self.region_update_queue = []