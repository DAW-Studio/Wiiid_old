import pygame
from util import Image

class MainScene():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = Image("interface.png", (0,0))

    def render(self):
        self.background.render(self.screen)
