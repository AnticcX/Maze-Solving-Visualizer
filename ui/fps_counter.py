""" 
FPS Counter for the Maze Solver application.
This module defines the FPSCounter class, which is a Pygame sprite that displays the current
frames per second (FPS) on the screen. The counter updates at a specified interval to provide real-time performance feedback to the user.
"""

import time as t

from pygame.sprite import Sprite
from pygame.font import Font
from pygame.time import Clock

# Make this a better visual
class FPSCounter(Sprite):
    def __init__(self, x: float, y: float,  clock: Clock, font: Font = None):
        super().__init__()
        if font:
            self.font = font
        else:
            self.font = Font(None, 16)
        self.clock = clock
        self.x = x
        self.y = y
        self.last_updated: float = t.time()
        
        self.image = self.font.render("FPS: 0", True, (255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def update(self) -> None:
        if t.time() - self.last_updated < .25: return None
        fps = str(int(self.clock.get_fps()))
        self.image = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_updated = t.time()
