import random, time

from typing import Optional, Tuple, List
from pygame import Surface, sprite, display
from pygame.time import Clock

from CONFIG import TILE_SIZE, MAZE_BACKGROUND_COLOR, DISPLAY_OFFSET
from components import Wall, Exit, Runner, Path
from ui.fpsCounter import FPSCounter

from algorithms.solvers.dfs_solver import solve_dfs

class Maze:
    def __init__(self, screen: Surface, clock: Clock, map_data: List[List[str]] = None):
        self.map_data: List[List[str]] = map_data
        self.cached_map_data = None
        self.screen: Surface = screen
        self.clock: Clock = clock
        
        self.all_sprites = sprite.RenderUpdates()
        self.background = Surface(screen.get_size())
        self.background.fill(MAZE_BACKGROUND_COLOR)
        
        self.all_sprites.add(FPSCounter(0, 0, self.clock))
        
        self.region_update_queue: list = []
        
        self.path_index = -1
        self.solved_maze = None
        
    def _update_screen(self) -> None:
        if not self.solved_maze or self.path_index < len(self.solved_maze['path']):
            self._walk_path()
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        self.region_update_queue.extend(self.all_sprites.draw(self.screen))
        display.update(self.region_update_queue)
        self.region_update_queue = []
        
    def _walk_path(self) -> None:
        if not self.solved_maze:
            self.solved_maze = solve_dfs(self.map_data)
        foot_path = self.solved_maze["path"]
        coordinate = foot_path[self.path_index]
        y, x = coordinate
        if self.map_data[y][x] != 'S' and self.map_data[y][x] != 'E':
            path = Path(x* TILE_SIZE + DISPLAY_OFFSET.x, y* TILE_SIZE + DISPLAY_OFFSET.y)
            self.background.blit(path.image, path.rect)
            self.region_update_queue.append(path.rect)
        self.path_index += 1
    
    def update(self) -> None:
        if self.cached_map_data == self.map_data: 
            self._update_screen()
            return None
        
        for row_i, row in enumerate(self.map_data):
            for col_i, char in enumerate(row):
                x = col_i * TILE_SIZE + DISPLAY_OFFSET.x
                y = row_i * TILE_SIZE + DISPLAY_OFFSET.y
                
                if char == '#':
                    wall = Wall(x, y)
                    self.background.blit(wall.image, wall.rect)
                    self.region_update_queue.append(wall.rect)
                elif char.lower() == 'e': 
                    exit = Exit(x, y)
                    self.all_sprites.add(exit)
                elif char.lower() == 's':
                    runner = Runner(x, y)
                    self.all_sprites.add(runner)
        
        self.cached_map_data = self.map_data
        self._update_screen()
    
    
    def generate_random_maze(
        self, 
        width: int, 
        height: int, 
        runner_start_pos: Optional[Tuple] = None, 
        end_pos: Optional[Tuple] = None) -> None:
        
        grid = [['#' for _ in range(width)] for _ in range(height)]
        visited = set()
        stack = []
        
        start_y, start_x = 1, 1
        grid[start_y][start_x] = '.'
        visited.add((start_y, start_x))
        stack.append((start_y, start_x))
        
        while stack:
            current_y, current_x = stack[-1]
            
            neighbors = []
            # Directions: (dy, dx)
            # Jumping 2 units to leap over the wall cell
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            
            for dy, dx in directions:
                ny, nx = current_y + dy, current_x + dx
                
                # Check bounds and if the destination cell is unvisited
                if 0 < ny < height - 1 and 0 < nx < width - 1 and (ny, nx) not in visited:
                    neighbors.append((ny, nx))
            
            if neighbors:
                walls_open = random.choices([1, 2, 3, 4], weights = [20, 20, 40, 10])
                    
                for _ in range(0, walls_open[0]):
                    try:
                        neighbor = random.choice(neighbors)
                        neighbors.remove(neighbor)
                        next_y, next_x = neighbor
                    
                        wall_y = (current_y + next_y) // 2
                        wall_x = (current_x + next_x) // 2
                        
                        grid[wall_y][wall_x] = '.' # Remove wall
                        grid[next_y][next_x] = '.' # Set destination as path
                        
                        visited.add((next_y, next_x))
                        stack.append((next_y, next_x))
                    except IndexError:
                        break
            else:
                # Backtrack
                stack.pop()
                
        if runner_start_pos:
            grid[runner_start_pos[1]][runner_start_pos[0]] = 'S'
        else:
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            grid[y][x] = 'S'
        if end_pos:
            grid[end_pos[1]][end_pos[0]] = 'E'
        else:
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            grid[y][x] = 'E'
            
        self.map_data = grid
        self._walk_path()