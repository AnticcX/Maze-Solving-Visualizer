from CONFIG import TILE_SIZE
from pygame.sprite import Sprite
from pygame import Surface


class Runner(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
