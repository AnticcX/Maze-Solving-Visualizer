from config import Tile, RUNNER_COLOR
from pygame.sprite import Sprite
from pygame import Surface


class Runner(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((Tile.size, Tile.size))
        self.image.fill(RUNNER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
