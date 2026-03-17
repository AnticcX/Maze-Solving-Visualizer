from typing import TypeAlias

from .solvers.dfs_solver import solve_dfs as internal_dfs_solve
from .solvers.bfs_solver import bfs as internal_bfs_solve

from .generators import randomized_dfs
from core.Types import Path, Grid

def solve_dfs(maze: Grid) -> tuple[Path, int, float, Path]:
    solved_data = internal_dfs_solve(maze)
    return solved_data['path'], solved_data['visited_count'], solved_data['runtime'], solved_data['path_history']

def solve_bfs(maze: Grid) -> tuple[Path, int, float, Path]:
    return internal_bfs_solve(maze)

__all__ = ['solve_dfs', 'solve_bfs', 'randomized_dfs']