import pygame
from util import Image

pygame.font.init()

class MainScene():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = Image("interface.png", (0,0))
        self.font = pygame.font.SysFont("Menlo",24)
        self.logs = []
        self.log("wiimote connected")

    def log(self, *args):
        self.logs.append(", ".join(args))


    def render(self):
        self.background.render(self.screen)
        height = 18
        for i, message in enumerate(self.logs):
            y = len(self.logs)-i
            self.screen.blit(self.font.render(message,1,(255,255,255)), (40,600-(height*y)))
