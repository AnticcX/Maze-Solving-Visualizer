"""
dfs_solver.py

Student B - DFS Engineer

Implements Depth-First Search (DFS) for maze solving.

Maze rules:
- 'S' = Start
- 'E' = End
- '#' = Wall
- '.' = Open path

Movement:
- Up, Down, Left, Right only
- No diagonal movement
"""

from time import perf_counter
from typing import List, Tuple, Dict, Optional

Coordinate = Tuple[int, int]
MazeGrid = List[List[str]]


def solve_dfs(maze: MazeGrid) -> Dict[str, object]:
    """
    Solve the maze using iterative DFS with an explicit stack.

    Args:
        maze: 2D list of characters

    Returns:
        A dictionary with:
        - found: bool
        - path: list of (row, col) coordinates from S to E
        - path_length: int
        - visited_count: int
        - runtime: float (seconds)
        - message: str
        - path_history: list of (row, col) coordinates of all paths traveled
    """
    start_time = perf_counter()
    if not maze or not maze[0]:
        return {
            "found": False,
            "path": [],
            "path_length": 0,
            "visited_count": 0,
            "runtime": 0.0,
            "message": "Invalid maze: empty grid.",
            "path_history": []
        }

    rows = len(maze)
    cols = len(maze[0])

    if not _is_rectangular(maze):
        return {
            "found": False,
            "path": [],
            "path_length": 0,
            "visited_count": 0,
            "runtime": 0.0,
            "message": "Invalid maze: rows have inconsistent lengths.",
            "path_history": []
        }

    start = _find_cell(maze, 'S')
    end = _find_cell(maze, 'E')

    if start is None: 
        return {
            "found": False,
            "path": [],
            "path_length": 0,
            "visited_count": 0,
            "runtime": 0.0,
            "message": "Invalid maze: missing start 'S'.",
            "path_history": []
        }

    if end is None:
        return {
            "found": False,
            "path": [],
            "path_length": 0,
            "visited_count": 0,
            "runtime": 0.0,
            "message": "Invalid maze: missing end 'E'.",
            "path_history": []
        }

    stack: List[Coordinate] = [start]
    path_history: List[Coordinate] = []
    visited = {start}
    parent: Dict[Coordinate, Optional[Coordinate]] = {start: None}
    visited_count = 0

    while stack:
        current = stack.pop()
        path_history.append(current)
        visited_count += 1

        if current == end:
            path = _reconstruct_path(parent, end)
            runtime = perf_counter() - start_time
            return {
                "found": True,
                "path": path,
                "path_length": len(path) - 1,
                "visited_count": visited_count,
                "runtime": runtime,
                "message": "Path found.",
                "path_history": path_history
            }

        for neighbor in _get_neighbors(current, rows, cols):
            r, c = neighbor
            if neighbor not in visited and maze[r][c] != '#':
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    runtime = perf_counter() - start_time
    return {
        "found": False,
        "path": [],
        "path_length": 0,
        "visited_count": visited_count,
        "runtime": runtime,
        "message": "No Path Found",
        "path_history": path_history
    }


def _find_cell(maze: MazeGrid, target: str) -> Optional[Coordinate]:
    """
    Find the first occurrence of target in the maze.
    Returns None if not found.
    """
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == target:
                return (r, c)
    return None


def _get_neighbors(cell: Coordinate, rows: int, cols: int) -> List[Coordinate]:
    """
    Return valid 4-direction neighbors in a fixed order:
    Up, Down, Left, Right
    """
    r, c = cell
    candidates = [
        (r - 1, c),  # Up
        (r + 1, c),  # Down
        (r, c - 1),  # Left
        (r, c + 1),  # Right
    ]

    neighbors = []
    for nr, nc in candidates:
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors


def _reconstruct_path(
    parent: Dict[Coordinate, Optional[Coordinate]],
    end: Coordinate
) -> List[Coordinate]:
    """
    Reconstruct path from start to end using parent links.
    """
    path = []
    current: Optional[Coordinate] = end

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def _is_rectangular(maze: MazeGrid) -> bool:
    """
    Check whether all rows have the same length.
    """
    if not maze:
        return False

    width = len(maze[0])
    return all(len(row) == width for row in maze)


def load_maze_from_lines(lines: List[str]) -> MazeGrid:
    """
    Convert a list of strings into a 2D maze grid.
    """
    return [list(line.strip()) for line in lines if line.strip()]


def load_maze_from_file(filepath: str) -> MazeGrid:
    """
    Load a maze from a text file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return load_maze_from_lines(lines)


if __name__ == "__main__":
    # -----------------------------
    # Test Case 1: Path exists
    # -----------------------------
    maze1 = [
        list("S...#"),
        list(".#.#."),
        list(".#..."),
        list(".###."),
        list("....E")
    ]

    result1 = solve_dfs(maze1)

    print("=== TEST CASE 1: PATH EXISTS ===")
    print("Found:", result1["found"])
    print("Path:", result1["path"])
    print("Path Length:", result1["path_length"])
    print("Visited Count:", result1["visited_count"])
    print("Runtime:", f"{result1['runtime']:.6f} seconds")
    print("Message:", result1["message"])
    print()

    # -----------------------------
    # Test Case 2: No path exists
    # -----------------------------
    maze2 = [
        list("S#."),
        list("###"),
        list(".#E")
    ]

    result2 = solve_dfs(maze2)

    print("=== TEST CASE 2: NO PATH ===")
    print("Found:", result2["found"])
    print("Path:", result2["path"])
    print("Path Length:", result2["path_length"])
    print("Visited Count:", result2["visited_count"])
    print("Runtime:", f"{result2['runtime']:.6f} seconds")
    print("Message:", result2["message"])
    print()

    # -----------------------------
    # Test Case 3: Stress test
    # -----------------------------
    maze3 = [
        list("S....#"),
        list(".##..#"),
        list(".#...#"),
        list(".###.#"),
        list("....E#")
    ]

    result3 = solve_dfs(maze3)

    print("=== TEST CASE 3: STRESS TEST ===")
    print("Found:", result3["found"])
    print("Path:", result3["path"])
    print("Path Length:", result3["path_length"])
    print("Visited Count:", result3["visited_count"])
    print("Runtime:", f"{result3['runtime']:.6f} seconds")
    print("Message:", result3["message"])