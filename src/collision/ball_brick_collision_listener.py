import pygame

from ..ball import Ball
from ..brick import Brick
from ..constants import BRICK_HIT_SOUND, Color
from ..rect import Rect
from .collision_listener import CollisionListener


class BallBrickCollisionListener(CollisionListener):
    def __init__(self):
        self.overlap = pygame.math.Vector2()
        self.brick_hit_sound = None

    def on_collision(self, a: Rect, b: Rect):
        if isinstance(a, Ball) and isinstance(b, Brick):
            ball = a
            brick = b
        elif isinstance(a, Brick) and isinstance(b, Ball):
            ball = b
            brick = a
        else:
            return

        Rect.calculate_overlap(ball, brick, self.overlap)
        self.overlap *= -1
        ball.rebound(self.overlap)

        brick.is_destroyed = True

        if not ball.is_orange_row_hit and brick.color == Color.ORANGE:
            ball.is_orange_row_hit = True
            ball.velocity.scale_to_length(ball.velocity.length() + ball.speed_increment)
        elif not ball.is_red_row_hit and brick.color == Color.RED:
            ball.is_red_row_hit = True
            ball.velocity.scale_to_length(
                ball.velocity.length() + ball.speed_increment * 2
            )

        if self.brick_hit_sound is None:
            self.brick_hit_sound = pygame.mixer.Sound(BRICK_HIT_SOUND)
        pygame.mixer.Sound.play(self.brick_hit_sound)
