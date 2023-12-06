import math

from ..ball import Ball
from ..paddle import Paddle
from ..rect import Rect
from .collision_listener import CollisionListener


class BallPaddleCollisionListener(CollisionListener):
    def on_collision(self, a: Rect, b: Rect):
        if isinstance(a, Ball) and isinstance(b, Paddle):
            ball = a
            paddle = b
        elif isinstance(a, Paddle) and isinstance(b, Ball):
            ball = b
            paddle = a
        else:
            return

        ball.bottom = paddle.top

        # calculate rebound angle
        ball_rebound_angle = (
            max(-1, min(1, (ball.centerx - paddle.centerx) / (paddle.width / 2)))
            * math.pi
            / 4
            - math.pi / 2
        )

        ball.velocity.x = ball.velocity.length() * math.cos(ball_rebound_angle)
        ball.velocity.y = ball.velocity.length() * math.sin(ball_rebound_angle)
