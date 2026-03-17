from config import Tile, WALL_COLOR
from pygame.sprite import Sprite
from pygame import Surface


""" 
Represents a wall in the maze.
The Wall class is a Pygame sprite that visually represents a wall in the maze. 
It is initialized with a specific position and displays a colored square to indicate the wall's location.
"""
class Wall(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((Tile.size, Tile.size))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
