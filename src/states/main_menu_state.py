import pygame

from .. import text
from ..constants import *
from ..state import BaseState, StateMachine


class MainMenuState(BaseState):
    def __init__(self, state_machine: StateMachine):
        super().__init__(state_machine)

        self.rendered = False

    def enter(self, scores: list[tuple[str, int]]):
        self.scores = scores

    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state_machine.change("MainGame")

    def render(self, screen: pygame.Surface):
        if not self.rendered:
            self.rendered = True

            screen.fill(Color.BLACK)

            text.render(screen, Color.GREY, "Highscores:", 100, 100)
            for i, (name, score) in enumerate(self.scores):
                text.render(
                    screen,
                    Color.GREY,
                    f"{i + 1}. {name} - {str(score).rjust(3, '0')}",
                    100,
                    140 + i * 30,
                )
            text.render(screen, Color.GREY, "Press Enter to Start", 100, 400)

            pygame.display.flip()
