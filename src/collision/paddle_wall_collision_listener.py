import pygame

from ..paddle import Paddle
from ..rect import Rect
from ..wall import Wall
from .collision_listener import CollisionListener


class PaddleWallCollisionListener(CollisionListener):
    def __init__(self):
        self.overlap = pygame.math.Vector2()

    def on_collision(self, a: Rect, b: Rect):
        if isinstance(a, Paddle) and isinstance(b, Wall):
            paddle = a
            wall = b
        elif isinstance(a, Wall) and isinstance(b, Paddle):
            paddle = b
            wall = a
        else:
            return

        Rect.calculate_overlap(paddle, wall, self.overlap)
        self.overlap *= -1
        paddle.left += self.overlap.x
