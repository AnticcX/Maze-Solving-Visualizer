from config import TILE_SIZE, WALL_COLOR
from pygame.sprite import Sprite
from pygame import Surface


class Wall(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
