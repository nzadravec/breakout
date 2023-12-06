import pygame

from ..ball import Ball
from ..rect import Rect
from ..wall import Wall
from .collision_listener import CollisionListener


class BallWallCollisionListener(CollisionListener):
    def __init__(self):
        self.overlap = pygame.math.Vector2()

    def on_collision(self, a: Rect, b: Rect):
        if isinstance(a, Ball) and isinstance(b, Wall):
            ball = a
            wall = b
        elif isinstance(a, Wall) and isinstance(b, Ball):
            ball = b
            wall = a
        else:
            return

        Rect.calculate_overlap(ball, wall, self.overlap)
        self.overlap *= -1
        ball.rebound(self.overlap)
