from config import Tile, EXIT_COLOR
from pygame.sprite import Sprite
from pygame import Surface

""" 
Represents the exit point in the maze.
The Exit class is a Pygame sprite that visually represents the exit location in the maze. 
It is initialized with a specific position and displays a colored square to indicate the exit. 
"""
class Exit(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((Tile.size, Tile.size))
        self.image.fill(EXIT_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
