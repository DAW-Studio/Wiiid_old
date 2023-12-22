import pygame
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Image:
    def __init__(self, name:str, pos:tuple[int,int]=(0,0)) -> None:
        self.surface = pygame.image.load(f"{DIR}/data/images/{name}")
        self.pos = pos

    def render(self, surface:pygame.Surface):
        surface.blit(self.surface, self.pos)
