import pygame

from .constants import *
from .rect import Rect
from .wall import Wall


class Paddle(Rect):
    def __init__(
        self,
        left: float = (WINDOW_WIGHT - PADDLE_WIDTH) // 2,
        top: float = WINDOW_HEIGHT - UNIT_LENGTH - PADDLE_HEIGHT // 2,
        width: float = PADDLE_WIDTH,
        height: float = PADDLE_HEIGHT,
        speed: float = PADDLE_SPEED,
        color: pygame.Color = Color.RED,
    ):
        super().__init__(left, top, width, height)

        self._initial_width = width
        self._speed = speed
        self._velocity = 0
        self._color = color

    def reset(self):
        self.width = self._initial_width

    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._velocity = -self._speed
            elif event.key == pygame.K_RIGHT:
                self._velocity = self._speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self._velocity = 0

    def update(self, delta_time: float):
        self.left += self._velocity * delta_time

    def hit(self, wall: Wall):
        overlap = Rect.calculate_overlap(self, wall)
        self.left -= overlap.x

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._color, self)
