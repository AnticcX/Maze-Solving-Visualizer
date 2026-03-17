import pygame

from dataclasses import dataclass
from pygame.font import Font, SysFont

from core.Types import RGB

pygame.font.init()

# Display settings
BACKGROUND_COLOR        : RGB = (0, 0, 0)

@dataclass
class ScreenSize:
    width               : int = 1650
    height              : int = 1030
    
@dataclass
class Panel:
    width               : int = 280
    height              : int = ScreenSize.height
    top_margin          : int = 20
    bottom_margin       : int = 80
    
@dataclass
class InputBox:
    background_color    : RGB = (235, 235, 235)
    active_color        : RGB = (255, 255, 255)
    border_color        : RGB = (200, 200, 200)
    active_border       : RGB = (120, 170, 255)

SELECTED_BFS_COLOR      : RGB = (0, 120, 255)
UNSELECTED_BFS_COLOR    : RGB = (120, 150, 200)
SELECTED_DFS_COLOR      : RGB = (0, 180, 100)
UNSELECTED_DFS_COLOR    : RGB = (120, 170, 140)
DEFAULT_BUTTON_COLOR    : RGB = (235, 235, 235)
BUTTON_TEXT_COLOR       : RGB = (40, 80, 180)
NO_PATH_TEXT_COLOR      : RGB = (180, 50, 50)
DFS_TEXT_COLOR          : RGB = (255, 255, 255)
BFS_TEXT_COLOR          : RGB = (255, 255, 255)

TITLE_FONT              : Font = SysFont(None, 42)
LABEL_FONT              : Font = SysFont(None, 30)
BUTTON_FONT             : Font = SysFont(None, 28)
STATS_FONT              : Font = SysFont(None, 34)

STATS_LABEL_GAP        : int = 35
STATS_START_Y_POS       : int = 670
    
# Maze config
@dataclass
class DisplayOffset:
    x                   : int = 0
    y                   : int = 0
    
@dataclass
class MazeSize:
    width               : int = 500
    height              : int = 500
    max_width           : int = 1000
    max_height          : int = 1000

MAZE_BACKGROUND_COLOR   : tuple = (100, 105, 100) # rgb value

# Sprite config
TILE_SIZE               : float = 1000 / ((MazeSize.width + MazeSize.height) / 2) # Pixel size of each grid square
GHOST_PATH_COLOR        : RGB = (40, 40, 55)
PATH_COLOR              : RGB = (255, 255, 0)
RUNNER_COLOR            : RGB = (255, 100, 255)
WALL_COLOR              : RGB = (20, 20, 20)
EXIT_COLOR              : RGB = (0, 255, 0)


# Simulation config
SIMULATION_SPEED        : int = 1 # How many tile paths are being drawn per each game tick
