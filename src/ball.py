import math
from typing import overload

import pygame

from .brick import Brick
from .constants import *
from .paddle import Paddle
from .rect import Rect
from .wall import Wall


class Ball(Rect):
    def __init__(
        self,
        midbottom: pygame.Vector2,
        radius: float = BALL_RADIUS,
        speed: float = BALL_SPEED,
        speed_increment: float = BALL_SPEED_INCREMENT,
        color: pygame.Color = Color.WHITE,
    ):
        super().__init__(0, 0, radius * 2, radius * 2)

        self._speed = speed
        self._speed_increment = speed_increment
        self._color = color
        self._velocity = pygame.Vector2()

        self.reset(midbottom)

    def reset(self, midbottom: pygame.Vector2):
        # TODO: randomize initial position
        self.midbottom = midbottom
        # TODO: randomize initial velocity
        self._velocity.x = 0
        self._velocity.y = -self._speed
        self._upper_wall_hit = False
        self._hits = 0
        self._orange_row_hit = False
        self._red_row_hit = False

    @property
    def upper_wall_hit(self) -> bool:
        return self._upper_wall_hit

    def update(self, delta_time: float):
        self.left += self._velocity.x * delta_time
        self.top += self._velocity.y * delta_time

    @overload
    def hit(self, rect: Paddle):
        ...

    @overload
    def hit(self, rect: Brick):
        ...

    @overload
    def hit(self, rect: Wall):
        ...

    def hit(self, rect: Rect):
        if isinstance(rect, Paddle):
            self._hit_paddle(rect)
        elif isinstance(rect, Brick):
            self._hit_brick(rect)
        elif isinstance(rect, Wall):
            self._hit_wall(rect)
        else:
            raise ValueError(f"Unsupported rectangle type: {type(rect)}")

        self._hits += 1
        if self._hits == 4 or self._hits == 12:
            self._velocity.scale_to_length(
                self._velocity.length() + self._speed_increment
            )

    def _hit_paddle(self, paddle: Paddle):
        self.bottom = paddle.top

        # calculate rebound angle
        ball_rebound_angle = (
            max(-1, min(1, (self.centerx - paddle.centerx) / (paddle.width / 2)))
            * math.pi
            / 4
            - math.pi / 2
        )
        self._velocity = self._velocity.length() * pygame.Vector2(
            math.cos(ball_rebound_angle), math.sin(ball_rebound_angle)
        )

    def _hit_brick(self, brick: Brick):
        overlap = Rect.calculate_overlap(self, brick)
        self._rebound(-overlap)

        if not self._orange_row_hit and brick.color == Color.ORANGE:
            self._orange_row_hit = True
            self._velocity.scale_to_length(
                self._velocity.length() + self._speed_increment
            )
        elif not self._red_row_hit and brick.color == Color.RED:
            self._red_row_hit = True
            self._velocity.scale_to_length(
                self._velocity.length() + self._speed_increment * 2
            )

    def _hit_wall(self, wall: Wall):
        overlap = Rect.calculate_overlap(self, wall)
        self._rebound(-overlap)

        if wall.upper:
            self._upper_wall_hit = True

    def _rebound(self, shift: pygame.Vector2):
        min_shift = min(abs(shift.x), abs(shift.y))
        if abs(shift.x) == min_shift:
            shift.y = 0
        else:
            shift.x = 0

        self.left += shift.x
        self.top += shift.y
        if shift.x != 0:
            self._velocity.x = math.copysign(self._velocity.x, shift.x)
        if shift.y != 0:
            self._velocity.y = math.copysign(self._velocity.y, shift.y)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._color, self)
