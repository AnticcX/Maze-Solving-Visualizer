import random
from typing import Optional, Literal, TypeAlias

from algorithms import solve_dfs, solve_bfs, randomized_dfs
from core.Types import Coordinate, MazeAlgorithm


class Maze:
    
    def __init__(self, width: Optional[int] = 10, height: Optional[int] = 10):
        self.width: int = width
        self.height: int = height
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
        algorithm: MazeAlgorithm = 'dfs'
        ) -> None:
        
        if algorithm == 'dfs': self.grid = randomized_dfs.generate(width, height, start_pos, end_pos)
        
    def solve(
        self, 
        algorithm: Optional[Literal['BFS', 'DFS']] = 'DFS'
        ) -> None:
        
        self.selected_algorithm = algorithm
        self.path, self.visited_count, self.runtime = solve_dfs(self.grid) if algorithm == 'DFS' else solve_bfs(self.grid) # ADD BFS option here when code is received 