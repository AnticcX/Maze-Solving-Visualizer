from dataclasses import dataclass

# Display settings
BACKGROUND_COLOR: tuple = (0, 0, 0)

@dataclass
class ScreenSize:
    width = 1650
    height = 1030
    
@dataclass
class Panel:
    width = 500
    height = 500
    top_margin = 20
    bottom_margin = 80
    
# Maze config
@dataclass
class DisplayOffset:
    x = 0
    y = 0
    
@dataclass
class MazeSize:
    width = 50
    height = 50
    max_width = 1000
    max_height = 1000

MAZE_BACKGROUND_COLOR: tuple = (100, 105, 100) # rgb value

# Sprite config
TILE_SIZE: int = 1000 / ((MazeSize.width + MazeSize.height) / 2) # Pixel size of each grid square
GHOST_PATH_COLOR: tuple = (40, 40, 55)
PATH_COLOR: tuple = (255, 255, 0)
RUNNER_COLOR: tuple = (255, 100, 255)
WALL_COLOR: tuple = (20, 20, 20)
EXIT_COLOR: tuple = (0, 255, 0)


# Simulation config
SIMULATION_SPEED = 1 # How many tile paths are being drawn per each game tick