from .ball_brick_collision_listener import BallBrickCollisionListener
from .ball_paddle_collision_listener import BallPaddleCollisionListener
from .ball_rect_collision_listener import BallRectCollisionListener
from .ball_wall_collision_listener import BallWallCollisionListener
from .collision_listener import CollisionListener
from .paddle_wall_collision_listener import PaddleWallCollisionListener

listeners: list[CollisionListener] = [
    BallBrickCollisionListener(),
    BallPaddleCollisionListener(),
    BallRectCollisionListener(),
    BallWallCollisionListener(),
    PaddleWallCollisionListener(),
]
