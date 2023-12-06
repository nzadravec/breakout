import pygame

from .rect import Rect


class DynamicRect(Rect):
    def __init__(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
        velocity: pygame.Vector2,
    ):
        super().__init__(left, top, width, height)

        self.velocity = velocity
