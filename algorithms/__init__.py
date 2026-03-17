from .solvers.dfs_solver import solve_dfs as internal_dfs_solve
from .solvers.bfs_solver import bfs as internal_bfs_solve

from .generators import randomized_dfs
from core.Types import Path, Grid


def solve_dfs(maze: Grid) -> tuple[Path, int, float, Path]:
    """Solves the maze using a depth-first search algorithm.

    Args:
        maze (Grid): The maze to solve.

    Returns:
        tuple[Path, int, float, Path]: A tuple containing the solution path, number of visited cells, runtime, and path history.
    """
    solved_data = internal_dfs_solve(maze)
    return solved_data['path'], solved_data['visited_count'], solved_data['runtime'], solved_data['path_history']

def solve_bfs(maze: Grid) -> tuple[Path, int, float, Path]:
    """Solves the maze using a breadth-first search algorithm.

    Args:
        maze (Grid): The maze to solve.

    Returns:
        tuple[Path, int, float, Path]: A tuple containing the solution path, number of visited cells, runtime, and path history.
    """
    return internal_bfs_solve(maze)

__all__ = ['solve_dfs', 'solve_bfs', 'randomized_dfs']