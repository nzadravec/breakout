from ..rect import Rect


class CollisionListener:
    def on_collision(self, a: Rect, b: Rect):
        raise NotImplementedError
