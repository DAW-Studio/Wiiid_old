import pygame
from util import Image

pygame.font.init()

class MainScene():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = Image("interface.png", (0,0))
        self.font = pygame.font.SysFont("Menlo",48)
        self.logHeight = 26
        self.maxLogs = 12
        self.logs = []
        self.log("wiimote connected")

    def log(self, *args):
        self.logs.append(", ".join([str(arg) for arg in args]))
        if len(self.logs) > self.maxLogs:
            self.logs.pop(0)


    def render(self):
        self.background.render(self.screen)
        for i, message in enumerate(self.logs):
            y = len(self.logs)-i
            self.screen.blit(self.font.render(message,1,(255,255,255)), (40,690-self.logHeight-(self.logHeight*y)))
