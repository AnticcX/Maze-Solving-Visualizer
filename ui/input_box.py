import pygame
from pygame import Surface
from pygame.event import Event
from pygame.font import Font
from typing import Optional

from config import InputBox as IB

class InputBox(IB):
    def __init__(self, x: int, y: int, width: int, height: int, text: Optional[str] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.active = False
            else:
                if event.unicode.isdigit() and len(self.text) < 3:
                    self.text += event.unicode

    def draw(self, screen: Surface, font: Font) -> None:
        pygame.draw.rect(
            screen,
            self.active_color if self.active else self.background_color,
            self.rect,
            border_radius=4
        )
        pygame.draw.rect(
            screen,
            self.active_border if self.active else self.border_color,
            self.rect,
            2,
            border_radius=4
        )

        txt_surface = font.render(self.text, True, (40, 40, 40))
        screen.blit(txt_surface, (self.rect.x + 8, self.rect.y + 10))