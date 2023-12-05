import pygame


class Rect:
    def __init__(self, left: float, top: float, width: float, height: float):
        self._left = left
        self._top = top
        self._width = width
        self._height = height

        # used to avoid creating new objects every frame
        self.rect = pygame.Rect(left, top, width, height)  # for drawing/rendering
        self._vec = pygame.Vector2()  # for non-primitive properties (e.g. midtop)

    @property
    def left(self) -> float:
        return self._left

    @left.setter
    def left(self, value: float):
        self._left = value
        self.rect.left = int(value)

    @property
    def top(self) -> float:
        return self._top

    @top.setter
    def top(self, value: float):
        self._top = value
        self.rect.top = int(value)

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = value
        self.rect.width = int(value)

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        self._height = value
        self.rect.height = int(value)

    @property
    def centerx(self) -> float:
        return self.left + self.width / 2

    @centerx.setter
    def centerx(self, value: float):
        self.left = value - self.width / 2

    @property
    def centery(self) -> float:
        return self.top + self.height / 2

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @bottom.setter
    def bottom(self, value: float):
        self.top = value - self.height

    @property
    def midtop(self) -> pygame.Vector2:
        self._vec.x = self.centerx
        self._vec.y = self.top
        return self._vec

    @midtop.setter
    def midtop(self, value: pygame.Vector2):
        self.centerx = value.x
        self.top = value.y

    @property
    def midbottom(self) -> pygame.Vector2:
        self._vec.x = self.centerx
        self._vec.y = self.bottom
        return self._vec

    @midbottom.setter
    def midbottom(self, value: pygame.Vector2):
        self.centerx = value.x
        self.bottom = value.y

    def hit(self, rect: "Rect"):
        pass

    def hit_by(self, rect: "Rect"):
        pass

    @staticmethod
    def colliderect(a: "Rect", b: "Rect") -> bool:
        """Return whether two rectangles intersect."""

        return (
            a.left < b.left + b.width
            and a.left + a.width > b.left
            and a.top < b.top + b.height
            and a.top + a.height > b.top
        )

    @staticmethod
    def calculate_overlap(kinematic: "Rect", static: "Rect"):
        """Calculate the overlap between two rectangles."""

        overlap = pygame.Vector2()
        if static.centerx < kinematic.centerx:
            overlap.x = kinematic.left - static.right
        else:
            overlap.x = kinematic.right - static.left
        if static.centery < kinematic.centery:
            overlap.y = kinematic.top - static.bottom
        else:
            overlap.y = kinematic.bottom - static.top
        return overlap
