from typing import Optional, Literal

from algorithms import solve_dfs, solve_bfs, randomized_dfs
from core.Types import Coordinate, MazeAlgorithm


class Maze:
    
    def __init__(self):
        self.grid: list[list[str]] = None
        
        # Values received from dfs/bfs solvers
        self.selected_algorithm: MazeAlgorithm = None
        self.path: list[tuple[int, int]] = None
        self.visited_count: int = None
        self.runtime: int = None
        self.solve_history: list[tuple[int, int]] = None
    
    def generate_random(
        self, 
        width: int, 
        height: int, 
        start_pos: Coordinate = None, 
        end_pos: Coordinate = None, 
        complexity: Optional[float] = 0.05,
        algorithm: MazeAlgorithm = 'DFS'
        ) -> None:
        
        if algorithm == 'DFS': self.grid = randomized_dfs.generate(width, height, start_pos, end_pos, complexity)
        
    def solve(
        self, 
        algorithm: Optional[Literal['BFS', 'DFS']] = 'DFS'
        ) -> None:
        
        self.selected_algorithm = algorithm
        self.path, self.visited_count, self.runtime, self.solve_history = solve_dfs(self.grid) if algorithm.lower() == 'dfs' else solve_bfs(self.grid)
    
    # surrounds the exit with walls to create a no path scenario for testing
    def block_exit(self): 
        actual_rows = len(self.grid)
        actual_cols = len(self.grid[0]) if actual_rows > 0 else 0
        
        # find E
        end_row, end_col = None, None
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'E':
                    end_row, end_col = r, c
                    break
            if end_row is not None:
                break
        
        # block E
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = end_row + dr, end_col + dc
            if 0 <= nr < actual_rows and 0 <= nc < len(self.grid[nr]):
                if self.grid[nr][nc] != 'S':
                    self.grid[nr][nc] = '#'