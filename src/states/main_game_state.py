from enum import Enum

import pygame

from .. import bricks, collision, digit
from ..ball import Ball
from ..brick import Brick
from ..constants import *
from ..paddle import Paddle
from ..state import BaseState, StateMachine
from ..wall import Wall


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

        self.walls: list[Wall] = []
        self.bricks: list[Brick] = []
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.midtop)

    def enter(self):
        self.score = 0
        self.health = 3
        self.level = 1
        self.state = InternalState.SERVE

        self.walls.append(Wall(0, UNIT_LENGTH, UNIT_LENGTH, WINDOW_HEIGHT))  # left wall
        self.walls.append(
            Wall(WINDOW_WIGHT - UNIT_LENGTH, UNIT_LENGTH, UNIT_LENGTH, WINDOW_HEIGHT)
        )  # right wall
        self.walls.append(
            Wall(0, UNIT_LENGTH, WINDOW_WIGHT, UNIT_LENGTH, True)
        )  # top/upper/back wall
        bricks.load(self.bricks)
        self.bricks_number = len(self.bricks)
        self.upper_wall_hit = False

    def exit(self):
        self.walls.clear()
        self.bricks.clear()

    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = InternalState.PLAY
        self.paddle.process(event)

    def update(self, delta_time: float):
        self.paddle.update(delta_time)
        for wall in self.walls:
            collision.resolve(self.paddle, wall)

        if self.state == InternalState.SERVE:
            self.serve_update(delta_time)
        elif self.state == InternalState.PLAY:
            self.play_update(delta_time)

    def serve_update(self, _: float):
        self.ball.midbottom = self.paddle.midtop

    def play_update(self, delta_time: float):
        self.ball.update(delta_time)
        if self.ball.top > WINDOW_HEIGHT:
            self.health -= 1
            self.paddle.reset()
            self.ball.reset(self.paddle.midtop)
            self.upper_wall_hit = False
            if self.health == 0:
                self.state_machine.change("GameOver", score=self.score)
            else:
                self.state = InternalState.SERVE
        else:
            collision.resolve(self.ball, self.paddle)
            for wall in self.walls:
                if (
                    collision.resolve(self.ball, wall)
                    and wall.upper
                    and not self.upper_wall_hit
                ):
                    self.upper_wall_hit = True
                    self.paddle.width /= 2
            for brick in self.bricks:
                if not brick.broken and collision.resolve(self.ball, brick):
                    self.bricks_number -= 1
                    self.score += brick.break_score
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

    def render(self, screen: pygame.Surface):
        screen.fill(Color.BLACK)

        self.render_hud(screen)
        for wall in self.walls:
            wall.render(screen)
        for brick in self.bricks:
            if not brick.broken:
                brick.render(screen)
        self.paddle.render(screen)
        self.ball.render(screen)

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
