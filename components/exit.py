from config import Tile, EXIT_COLOR
from pygame.sprite import Sprite
from pygame import Surface


class Exit(Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.image: Surface = Surface((Tile.size, Tile.size))
        self.image.fill(EXIT_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
