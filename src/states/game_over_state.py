import pygame

from .. import scores, text
from ..constants import *
from ..state import BaseState, StateMachine


class GameOverState(BaseState):
    def __init__(self, state_machine: StateMachine):
        super().__init__(state_machine)

        self.rerender = True

    def enter(self, score: int):
        self.score = score
        self.name: list[str] = []

        self.scores = scores.load()
        self.high_score_index = -1
        for i, (_, score) in enumerate(self.scores):
            if self.score > score:
                self.high_score_index = i
                break
        else:
            self.state_machine.change("MainMenu", scores=self.scores)

    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if (
                event.key >= pygame.K_a
                and event.key <= pygame.K_z
                and len(self.name) < 3
            ):
                self.name.append(chr(event.key).upper())

            elif event.key == pygame.K_BACKSPACE and len(self.name) > 0:
                self.name.pop()

            elif event.key == pygame.K_RETURN and len(self.name) == 3:
                self.scores.insert(
                    self.high_score_index, ("".join(self.name), self.score)
                )
                self.scores.pop()
                scores.save(self.scores)
                self.state_machine.change("MainMenu", scores=self.scores)

            self.rerender = True

    def render(self, screen: pygame.Surface):
        if self.rerender:
            screen.fill(Color.BLACK)

            text.render(screen, Color.RED, "New Highscore!", 60, 40)
            text.render(screen, Color.GREY, "Name:", 100, 100)
            pygame.draw.line(screen, Color.GREY, (110, 240), (140, 240), 2)
            pygame.draw.line(screen, Color.GREY, (150, 240), (180, 240), 2)
            pygame.draw.line(screen, Color.GREY, (190, 240), (220, 240), 2)

            if len(self.name) == 0:
                pygame.draw.rect(screen, Color.GREY, (110, 200, 3, 36))
            elif len(self.name) == 1:
                pygame.draw.rect(screen, Color.GREY, (150, 200, 3, 36))
                text.render(screen, Color.GREY, self.name[0], 110, 200)
            elif len(self.name) == 2:
                pygame.draw.rect(screen, Color.GREY, (190, 200, 3, 36))
                text.render(screen, Color.GREY, self.name[0], 110, 200)
                text.render(screen, Color.GREY, self.name[1], 150, 200)
            elif len(self.name) == 3:
                text.render(screen, Color.GREY, self.name[0], 110, 200)
                text.render(screen, Color.GREY, self.name[1], 150, 200)
                text.render(screen, Color.GREY, self.name[2], 190, 200)

            pygame.display.flip()
