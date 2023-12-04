import pygame
import sys

RPT_BTN = None
BTN_A = pygame.K_a
BTN_B = pygame.K_b
BTN_UP = pygame.K_UP
BTN_DOWN = pygame.K_DOWN
BTN_LEFT = pygame.K_LEFT
BTN_RIGHT = pygame.K_RIGHT
BTN_PLUS = pygame.K_EQUALS
BTN_MINUS = pygame.K_MINUS
BTN_HOME = pygame.K_h
BTN_1 = pygame.K_1
BTN_2 = pygame.K_2


class Wiimote():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Wiiid Dev")
        self.state = {
            "buttons": 0
        }


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.state["buttons"] = event.key
            if event.type == pygame.KEYUP:
                self.state["buttons"] = 0

        pygame.display.update()
                

