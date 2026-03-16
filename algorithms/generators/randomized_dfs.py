from typing import Optional
from random import choice, random

from core.Types import Coordinate, Grid


def generate(
    width: int, 
    height: int, 
    start_pos: Optional[Coordinate] = None, 
    end_pos: Optional[Coordinate] = None, 
    complexity: float = 0.05
    ) -> Grid:
    
    grid = [['#' for _ in range(width)] for _ in range(height)]
    visited = set()
    stack = []
        
    start_y, start_x = 1, 1
    grid[start_y][start_x] = '.'
    visited.add((start_y, start_x))
    stack.append((start_y, start_x))
    
    # generate a perfect, one solution maze
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
            next_y, next_x = choice(neighbors)
            
            wall_y = (current_y + next_y) // 2
            wall_x = (current_x + next_x) // 2
            
            grid[wall_y][wall_x] = '.' # Remove wall
            grid[next_y][next_x] = '.' # Set destination as path
            
            visited.add((next_y, next_x))
            stack.append((next_y, next_x))
        else:
            # Backtrack
            stack.pop()
    
    # create multiple paths
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if grid[y][x] == '#':
                is_horizontal_wall = grid[y][x-1] == '.' and grid[y][x+1] == '.'
                is_vertical_wall = grid[y-1][x] == '.' and grid[y+1][x] == '.'
                
                if is_horizontal_wall or is_vertical_wall:
                    if random() < complexity:
                        grid[y][x] = '.'
            
    if start_pos:   grid = place_start(grid, start_pos)
    else:           grid = place_start(grid)
        
    if not end_pos:
        # subtracted by 3 so its not in the maze outer boundary. 
        end_pos = (width - 3, height - 3)
    grid = place_exit(grid, end_pos)
        
    return grid

def place_start(grid: Grid, pos: Optional[Coordinate] = (1, 1)) -> Grid:
    x, y = pos
    grid[y][x] = 'S'
    return grid
    
def place_exit(grid: Grid, pos: Coordinate) -> Grid:
    x, y = pos
    grid[y][x] = 'E'
    return grid
