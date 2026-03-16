from dataclasses import dataclass

# Display settings
BACKGROUND_COLOR: tuple = (0, 0, 0)

@dataclass
class ScreenSize:
    _width = 1650
    _height = 1030
    
# Maze config
@dataclass
class DisplayOffset:
    _x = 15
    _y = 15
    
@dataclass
class MaxMazeSize:
    _width = 100
    _height = 100

MAZE_BACKGROUND_COLOR: tuple = (100, 105, 100) # rgb value

# Sprite config
TILE_SIZE: int = 1000 / ((MaxMazeSize._width + MaxMazeSize._height) / 2) # Pixel size of each grid square
GHOST_PATH_COLOR: tuple = (40, 40, 55)
PATH_COLOR: tuple = (255, 255, 0)
RUNNER_COLOR: tuple = (255, 100, 255)
WALL_COLOR: tuple = (20, 20, 20)
EXIT_COLOR: tuple = (0, 255, 0)


# Simulation config
SIMULATION_SPEED = 10 # How many tile paths are being drawn per each game tick