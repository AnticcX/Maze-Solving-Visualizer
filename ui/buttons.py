from dataclasses import dataclass
from pygame import Rect

from ui.input_box import InputBox
from config import MazeSize, SIMULATION_SPEED

@dataclass
class Buttons:
    rows_input_box      = InputBox(25, 95, 210, 42, str(MazeSize.width))
    columns_input_box   = InputBox(25, 185, 210, 42, str(MazeSize.height))
    speed_input_box     = InputBox(25, 275, 210, 42, str(SIMULATION_SPEED)) 
    bfs                 = Rect(25, 335, 100, 44)
    dfs                 = Rect(135, 335, 100, 44)
    generate            = Rect(25, 395, 220, 44)
    solve               = Rect(25, 455, 220, 44)
    reset               = Rect(25, 525, 220, 44)
    no_path             = Rect(25, 595, 220, 44)