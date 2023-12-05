from typing import Union, overload

from .ball import Ball
from .brick import Brick
from .paddle import Paddle
from .rect import Rect
from .wall import Wall

Dynamic = Union[Ball, Paddle]
Static = Union[Paddle, Wall, Brick]


@overload
def resolve(dynamic: Ball, static: Paddle) -> bool:
    ...


@overload
def resolve(dynamic: Ball, static: Wall) -> bool:
    ...


@overload
def resolve(dynamic: Ball, static: Brick) -> bool:
    ...


@overload
def resolve(dynamic: Paddle, static: Wall) -> bool:
    ...


def resolve(dynamic: Rect, static: Rect) -> bool:
    if Rect.colliderect(dynamic, static):
        dynamic.hit(static)
        static.hit_by(dynamic)
        return True
    return False
