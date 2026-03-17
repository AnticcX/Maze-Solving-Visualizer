from config import Tile, GHOST_PATH_COLOR
from pygame.sprite import Sprite
from pygame import Surface

""" 
Represents the path taken by the solver in the maze. (For historical visualization)
The GhostPath class is a Pygame sprite that visually represents the path taken by the maze
solver. It is initialized with a specific position and displays a colored square to indicate the path.
"""
class GhostPath(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((Tile.size, Tile.size))
        self.image.fill(GHOST_PATH_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
