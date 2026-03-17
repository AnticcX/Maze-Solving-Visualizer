from typing import TypeAlias, Optional, Literal

Grid            : TypeAlias = list[list[str]]
Coordinate      : TypeAlias = tuple[int, int]
Path            : TypeAlias = list[tuple[int, int]]
RGB             : TypeAlias = tuple[int, int, int]
MazeAlgorithm   : TypeAlias = Optional[Literal['dfs', 'bfs']]