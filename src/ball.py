import math

import pygame

from .constants import *
from .dynamic_rect import DynamicRect


class Ball(DynamicRect):
    def __init__(
        self,
        midbottom: pygame.Vector2,
        radius: float = BALL_RADIUS,
        speed: float = BALL_SPEED,
        speed_increment: float = BALL_SPEED_INCREMENT,
        color: pygame.Color = Color.WHITE,
    ):
        super().__init__(0, 0, radius * 2, radius * 2, pygame.Vector2())

        self._speed = speed
        self.speed_increment = speed_increment
        self._color = color

        self.reset(midbottom)

    def reset(self, midbottom: pygame.Vector2):
        # TODO: randomize initial position
        self.midbottom = midbottom
        # TODO: randomize initial velocity
        self.velocity.x = 0
        self.velocity.y = -self._speed
        self.hits = 0
        self.is_orange_row_hit = False
        self.is_red_row_hit = False

    def rebound(self, shift: pygame.Vector2):
        min_shift = min(abs(shift.x), abs(shift.y))
        if abs(shift.x) == min_shift:
            shift.y = 0
        else:
            shift.x = 0

        self.left += shift.x
        self.top += shift.y
        if shift.x != 0:
            self.velocity.x = math.copysign(self.velocity.x, shift.x)
        if shift.y != 0:
            self.velocity.y = math.copysign(self.velocity.y, shift.y)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._color, self)
