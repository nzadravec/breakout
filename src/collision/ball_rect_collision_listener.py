from ..ball import Ball
from ..rect import Rect
from .collision_listener import CollisionListener


class BallRectCollisionListener(CollisionListener):
    def on_collision(self, a: Rect, b: Rect):
        if isinstance(a, Ball):
            ball = a
        elif isinstance(b, Ball):
            ball = b
        else:
            return

        ball.hits += 1
        if ball.hits == 4 or ball.hits == 12:
            ball.velocity.scale_to_length(ball.velocity.length() + ball.speed_increment)
