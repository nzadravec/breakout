from typing import Any, Type

import pygame


class BaseState:
    def __init__(self, state_machine: "StateMachine"):
        self.state_machine = state_machine

    def enter(self, **params: Any):
        pass

    def exit(self):
        pass

    def process(self, event: pygame.event.Event):
        pass

    def update(self, delta_time: float):
        pass

    def render(self, screen: pygame.Surface):
        pass


class StateMachine:
    def __init__(self, states: dict[str, Type[BaseState]]):
        self.empty = BaseState(self)
        self.states = states or {}  # [name] -> [function that returns states]
        self.current = self.empty

    def change(self, state_name: str, **enter_params: Any):
        assert self.states[state_name]  # state must exist!
        self.current.exit()
        self.current = self.states[state_name](self)
        self.current.enter(**enter_params)

    def process(self, event: pygame.event.Event):
        self.current.process(event)

    def update(self, delta_time: float):
        self.current.update(delta_time)

    def render(self, screen: pygame.Surface):
        self.current.render(screen)
