import pygame

from .constants import *
from .dynamic_rect import DynamicRect


class Paddle(DynamicRect):
    def __init__(
        self,
        left: float = (WINDOW_WIDTH - PADDLE_WIDTH) // 2,
        top: float = WINDOW_HEIGHT - UNIT_LENGTH - PADDLE_HEIGHT,
        width: float = PADDLE_WIDTH,
        height: float = PADDLE_HEIGHT,
        speed: float = PADDLE_SPEED,
        color: pygame.Color = Color.RED,
    ):
        super().__init__(left, top, width, height, pygame.Vector2())

        self._initial_width = width
        self._speed = speed
        self._color = color

    def reset(self):
        self.width = self._initial_width

    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity.x -= self._speed
            elif event.key == pygame.K_RIGHT:
                self.velocity.x += self._speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.velocity.x += self._speed
            elif event.key == pygame.K_RIGHT:
                self.velocity.x -= self._speed

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._color, self)
