from typing import Optional, Literal

from algorithms import solve_dfs, solve_bfs, randomized_dfs
from core.Types import Coordinate, MazeAlgorithm

""" 
Maze class for representing the maze structure and managing its state.
The Maze class encapsulates the maze grid, the selected pathfinding algorithm, and the results of solving the maze. 
It provides methods for generating random mazes, solving the maze using different algorithms,
and modifying the maze structure (e.g., blocking the exit). The class is designed
"""
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
        algorithm: Optional[MazeAlgorithm] = 'DFS'
        ) -> None:
        """Generates a random maze utilizing the specified algorithm and parameters, and updates the maze grid accordingly.

        Args:
            width (int): The width of the maze to generate.
            height (int): The height of the maze to generate.
            start_pos (Coordinate, optional): The starting position for the maze. Defaults to None.
            end_pos (Coordinate, optional): The ending position for the maze. Defaults to None.
            complexity (float, optional): A value between 0 and 1 that determines the complexity of the generated maze. Defaults to 0.05.
            algorithm (MazeAlgorithm, optional): The algorithm to use for generating the maze.
        """
        if algorithm == 'DFS': self.grid = randomized_dfs.generate(width, height, start_pos, end_pos, complexity)
        
    def solve(
        self, 
        algorithm: Optional[Literal['BFS', 'DFS']] = 'DFS'
        ) -> None:
        """Solves the maze using the specified pathfinding algorithm (DFS or BFS) and updates the maze's path, visited count, runtime, and solve history.

        Args:
            algorithm (Literal['BFS', 'DFS'], optional): The pathfinding algorithm to use for solving the maze. Defaults to 'DFS'.
        """
        self.selected_algorithm = algorithm
        self.path, self.visited_count, self.runtime, self.solve_history = solve_dfs(self.grid) if algorithm.lower() == 'dfs' else solve_bfs(self.grid)
    
    def block_exit(self): 
        """Surrounds the exit with walls to create a no path scenario, effectively blocking access to the exit in the maze.
        """
        actual_rows = len(self.grid)
        
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