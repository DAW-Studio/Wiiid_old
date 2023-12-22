from .scene import Scene, pygame
from util import Image


class ConnectScene():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = Image("scenes/connect/background.png")

    def render(self):
        self.background.render(self.screen)
