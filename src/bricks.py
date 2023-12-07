from .brick import Brick
from .constants import *


def load(
    bricks: list[Brick],
    bricks_layer_centerx: int = WINDOW_WIDTH // 2,
    bricks_layer_centery: int = int(UNIT_LENGTH * 3.5) + BRICK_HEIGHT * 3,
    brick_width: int = BRICK_WIDTH,
    brick_height: int = BRICK_HEIGHT,
):
    row_count = 6
    column_count = 18
    bricks_layer_width = column_count * brick_width
    bricks_layer_height = row_count * brick_height
    bricks_layer_left = bricks_layer_centerx - bricks_layer_width / 2
    bricks_layer_top = bricks_layer_centery - bricks_layer_height / 2
    for i in range(row_count):
        for j in range(column_count):
            bricks.append(
                Brick(
                    bricks_layer_left + j * brick_width,
                    bricks_layer_top + i * brick_height,
                    BRICK_ROW_TO_SCORE[i],
                    BRICK_ROW_TO_COLOR[i],
                )
            )
