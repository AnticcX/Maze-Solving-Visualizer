from config import TILE_SIZE, PATH_COLOR
from pygame.sprite import Sprite
from pygame import Surface


class Path(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(PATH_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
