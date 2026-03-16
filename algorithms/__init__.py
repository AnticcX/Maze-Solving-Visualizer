from typing import TypeAlias

from .solvers.dfs_solver import solve_dfs as internal_solve

from .generators import randomized_dfs
from core.Types import Path, Coordinate, Grid

def solve_dfs(maze: Grid) -> tuple[Path, int, float]:
    solved_data = internal_solve(maze)
    return solved_data['path'], solved_data['visited_count'], solved_data['runtime']

__all__ = ['solve_dfs', 'randomized_dfs']