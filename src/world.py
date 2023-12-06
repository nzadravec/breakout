from typing import Callable

from .dynamic_rect import DynamicRect
from .rect import Rect


class World:
    def __init__(self, collision_callback: Callable[[Rect, Rect], None]):
        self.collision_callback = collision_callback
        self.static_rects: list[Rect] = []
        self.dynamic_rects: list[DynamicRect] = []

    def update(self, delta_time: float):
        for dynamic_rect in self.dynamic_rects:
            if not dynamic_rect.is_destroyed:
                dynamic_rect.left += dynamic_rect.velocity.x * delta_time
                dynamic_rect.top += dynamic_rect.velocity.y * delta_time

                for static_rect in self.static_rects:
                    if not static_rect.is_destroyed and Rect.colliderect(
                        dynamic_rect, static_rect
                    ):
                        self.collision_callback(dynamic_rect, static_rect)

                for other_dynamic_rect in self.dynamic_rects:
                    if dynamic_rect is not other_dynamic_rect:
                        if not other_dynamic_rect.is_destroyed and Rect.colliderect(
                            dynamic_rect, other_dynamic_rect
                        ):
                            self.collision_callback(dynamic_rect, other_dynamic_rect)
