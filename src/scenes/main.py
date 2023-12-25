import pygame
from util import Image

pygame.font.init()

class MainScene():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = Image("interface.png", (0,0))
        self.font = pygame.font.SysFont("Menlo",24)
        self.logs = []
        self.log("hello")

    def log(self, *args):
        self.logs.append(str(args))


    def render(self):
        self.background.render(self.screen)
        height = 12
        for i, message in enumerate(self.logs):
            self.screen.blit(self.font.render(message,1,(255,255,255)), (40,height*i+40))
