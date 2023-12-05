import pygame

from .constants import *
from .rect import Rect


class Brick(Rect):
    @classmethod
    @property
    def brick_sound(cls):
        return pygame.mixer.Sound(BRICK_HIT_SOUND)

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

        self._broken = False
        self.break_score = break_score
        self.color = color

    @property
    def broken(self) -> bool:
        return self._broken

    def hit_by(self, ball: Rect):
        self._broken = True
        pygame.mixer.Sound.play(self.brick_sound)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self)
