class Color:
    import pygame

    WHITE = pygame.Color("#FFFFFF")
    BLACK = pygame.Color("#000000")
    GREY = pygame.Color("#8E8E8E")
    RED = pygame.Color("#c84848")
    ORANGE = pygame.Color("#c66c3a")
    BROWN = pygame.Color("#b47a30")
    YELLOW = pygame.Color("#a2a22a")
    GREEN = pygame.Color("#48a048")
    BLUE = pygame.Color("#4248c8")


SCALE_FACTOR = 5


WINDOW_WIGHT = SCALE_FACTOR * 160
WINDOW_HEIGHT = SCALE_FACTOR * 105

# used for HUD height, wall thickess, paddle bottom margin, etc.
UNIT_LENGTH = SCALE_FACTOR * 8

PADDLE_WIDTH = SCALE_FACTOR * 16
PADDLE_HEIGHT = SCALE_FACTOR * 2
PADDLE_SPEED = SCALE_FACTOR * 115

BALL_RADIUS = SCALE_FACTOR
BALL_SPEED = SCALE_FACTOR * 40
BALL_SPEED_INCREMENT = SCALE_FACTOR * 8

BRICK_WIDTH = SCALE_FACTOR * 8
BRICK_HEIGHT = SCALE_FACTOR * 3
BRICK_ROW_TO_COLOR = [
    Color.RED,
    Color.ORANGE,
    Color.BROWN,
    Color.YELLOW,
    Color.GREEN,
    Color.BLUE,
]  # colors of bricks in each row
BRICK_ROW_TO_SCORE = [7, 7, 4, 4, 1, 1]  # score for breaking a brick in each row
BRICK_HIT_SOUND = "sounds/brick-hit.wav"

HUD_SCORE_LEFTPOS = int(4.5 * UNIT_LENGTH)
HUD_HEALTH_LEFTPOS = int(12.5 * UNIT_LENGTH)
HUD_LEVEL_LEFTPOS = int(16.5 * UNIT_LENGTH)
