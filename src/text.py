import pygame

_font = None


def render(screen: pygame.Surface, color: pygame.Color, text: str, x: int, y: int):
    global _font
    if _font is None:
        _font = pygame.font.Font("fonts/PressStart2P.ttf", 24)
    source = _font.render(text, False, color)
    dest = source.get_rect()
    dest.topleft = (x, y)
    screen.blit(source, dest)
