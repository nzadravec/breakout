import pygame

from src import scores
from src.constants import *
from src.state import StateMachine
from src.states import GameOverState, MainGameState, MainMenuState


class Game:
    def __init__(self):
        pygame.display.set_caption("Breakout")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.state_machine = StateMachine(
            {
                "MainMenu": MainMenuState,
                "MainGame": MainGameState,
                "GameOver": GameOverState,
            }
        )
        self.state_machine.change("MainMenu", scores=scores.load())

    def process(self, event: pygame.event.Event):
        self.state_machine.process(event)

    def update(self, delta_time: float):
        # prevent the ball from moving too far in one frame and passing through walls
        # when game is not focused or is in debug mode
        if delta_time > 0.1:
            return

        self.state_machine.update(delta_time)

    def render(self):
        self.state_machine.render(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                self.process(event)

            delta_time = self.clock.tick(60) / 1000.0

            self.update(delta_time)
            self.render()


if __name__ == "__main__":
    pygame.init()
    Game().run()
    pygame.quit()
