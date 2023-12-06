from enum import Enum

import pygame

from .. import bricks, collision, digit
from ..ball import Ball
from ..brick import Brick
from ..constants import *
from ..paddle import Paddle
from ..rect import Rect
from ..state import BaseState, StateMachine
from ..wall import Wall
from ..world import World


class InternalState(Enum):
    SERVE = 0
    PLAY = 1


class MainGameState(BaseState):
    def __init__(self, state_machine: StateMachine):
        super().__init__(state_machine)

        self.score = 0
        self.health = 0
        self.level = 0
        self.state = InternalState.SERVE

        walls: list[Wall] = [
            Wall(0, UNIT_LENGTH, UNIT_LENGTH, WINDOW_HEIGHT),  # left wall
            Wall(
                WINDOW_WIDTH - UNIT_LENGTH, UNIT_LENGTH, UNIT_LENGTH, WINDOW_HEIGHT
            ),  # right wall
            Wall(
                0, UNIT_LENGTH, WINDOW_WIDTH, UNIT_LENGTH, is_upper=True
            ),  # top/upper/back wall
            Wall(
                0, WINDOW_HEIGHT, WINDOW_WIDTH, UNIT_LENGTH, is_lower=True
            ),  # bottom/lower/front/death wall
        ]
        self.bricks: list[Brick] = []
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.midtop)

        def on_ball_brick_collision(a: Rect, b: Rect):
            if isinstance(a, Ball) and isinstance(b, Brick):
                brick = b
            elif isinstance(a, Brick) and isinstance(b, Ball):
                brick = a
            else:
                return

            self.score += brick.break_score
            self.bricks_number -= 1

            if self.bricks_number == 0:
                if self.level == 2:
                    self.state_machine.change("GameOver", score=self.score)
                else:
                    self.level += 1
                    self.state = InternalState.SERVE

                    self.bricks.clear()
                    bricks.load(self.bricks)
                    self.bricks_number = len(self.bricks)
                    self.paddle.reset()
                    self.ball.reset(self.paddle.midtop)
                    self.upper_wall_hit = False

        def on_ball_upper_wall_collision(a: Rect, b: Rect):
            if isinstance(a, Ball) and isinstance(b, Wall):
                wall = b
            elif isinstance(a, Wall) and isinstance(b, Ball):
                wall = a
            else:
                return

            if wall.is_upper and not self.upper_wall_hit:
                self.upper_wall_hit = True
                self.paddle.width /= 2

        def on_ball_lower_wall_collision(a: Rect, b: Rect):
            if isinstance(a, Ball) and isinstance(b, Wall):
                wall = b
            elif isinstance(a, Wall) and isinstance(b, Ball):
                wall = a
            else:
                return

            if wall.is_lower:
                self.health -= 1
                self.paddle.reset()
                self.ball.reset(self.paddle.midtop)
                self.upper_wall_hit = False
                if self.health == 0:
                    self.state_machine.change("GameOver", score=self.score)
                else:
                    self.state = InternalState.SERVE

        def collision_callback(a: Rect, b: Rect):
            for listener in collision.listeners:
                listener.on_collision(a, b)
            on_ball_brick_collision(a, b)
            on_ball_upper_wall_collision(a, b)
            on_ball_lower_wall_collision(a, b)

        self.world = World(collision_callback)
        for wall in walls:
            self.world.static_rects.append(wall)
        self.world.dynamic_rects.append(self.paddle)
        self.world.dynamic_rects.append(self.ball)

    def enter(self):
        self.score = 0
        self.health = 3
        self.level = 1
        self.state = InternalState.SERVE

        bricks.load(self.bricks)
        self.bricks_number = len(self.bricks)
        self.upper_wall_hit = False
        for brick in self.bricks:
            self.world.static_rects.append(brick)

    def exit(self):
        pass

    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = InternalState.PLAY
        self.paddle.process(event)

    def update(self, delta_time: float):
        self.world.update(delta_time)

        if self.state == InternalState.SERVE:
            self.ball.midbottom = self.paddle.midtop

    def render(self, screen: pygame.Surface):
        screen.fill(Color.BLACK)

        self.render_hud(screen)
        for static_rect in self.world.static_rects:
            if not static_rect.is_destroyed:
                static_rect.render(screen)
        for dynamic_rect in self.world.dynamic_rects:
            if not dynamic_rect.is_destroyed:
                dynamic_rect.render(screen)

        pygame.display.flip()

    def render_hud(self, screen: pygame.Surface):
        # NOTE: expect 3 digits for score, 1 digit for health, 1 digit for level
        for i, n in enumerate(range(2, -1, -1)):
            digit.render(
                screen,
                Color.GREY,
                self.score // 10**n % 10,
                HUD_SCORE_LEFTPOS + i * UNIT_LENGTH * 2,
                UNIT_LENGTH // 4,
            )
        digit.render(
            screen, Color.GREY, self.health, HUD_HEALTH_LEFTPOS, UNIT_LENGTH // 4
        )
        digit.render(
            screen, Color.GREY, self.level, HUD_LEVEL_LEFTPOS, UNIT_LENGTH // 4
        )
