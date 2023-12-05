import os

import pygame

from .constants import *


def _load() -> dict[int, list[pygame.Rect]]:
    dir = "fonts/digits"
    digits: dict[int, list[pygame.Rect]] = {}
    for p in os.listdir(dir):
        digit = int(os.path.splitext(p)[0])
        digits[digit] = []
        with open(os.path.join(dir, p), "r") as fp:
            os.path.basename(fp.name)
            for i, l in enumerate(fp.readlines()):
                for j, c in enumerate(l.rstrip("\n")):
                    if c == "#":
                        digits[digit].append(
                            pygame.Rect(
                                UNIT_LENGTH // 2 * j,
                                UNIT_LENGTH // 8 * i,
                                UNIT_LENGTH // 2,
                                UNIT_LENGTH // 8,
                            )
                        )
    return digits


_digits = _load()


def render(screen: pygame.Surface, color: pygame.Color, digit: int, x: int, y: int):
    for rect in _digits[digit]:
        rect.left += x
        rect.top += y
        pygame.draw.rect(screen, color, rect)
        rect.left -= x
        rect.top -= y
