import pygame

from .constants import *
from .rect import Rect


class Wall(Rect):
    def __init__(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
        is_upper: bool = False,
        is_lower: bool = False,
        color: pygame.Color = Color.GREY,
    ):
        super().__init__(left, top, width, height)

        self.is_upper = is_upper
        self.is_lower = is_lower
        self._color = color

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._color, self)
