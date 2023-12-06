import pygame

from .constants import *
from .rect import Rect


class Brick(Rect):
    def __init__(
        self,
        left: float,
        top: float,
        break_score: int,
        color: pygame.Color,
        width: float = BRICK_WIDTH,
        height: float = BRICK_HEIGHT,
    ):
        super().__init__(left, top, width, height)

        self.break_score = break_score
        self.color = color

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self)
