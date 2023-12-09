import pygame
import sys
import os
import json
import time

pygame.init()

DIR = os.path.dirname(os.path.abspath(__file__))

class Image:
    def __init__(self, name:str, pos:tuple[int,int]) -> None:
        self.surface = pygame.image.load(f"{DIR}/data/images/{name}")
        self.pos = pos

    def render(self, surface:pygame.Surface):
        surface.blit(self.surface, self.pos)


class Button:
    def __init__(self, ID:int, name:str, pos:tuple[int,int], value:int=0, holdtime:float=-1):
        self.ID = ID
        self.value = value
        self.holdtime = holdtime
        self.holding = False
        self.image = Image(f"{name}.png", pos)




class DevWiiid:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((720,720))
        pygame.display.set_caption("DevWiiid")
        self.base_top = Image("base_top.png", (220,90))
        self.base_bottom = Image("base_bottom.png", (374,90))
        self.buttons = {
            "a": Button(pygame.K_a, "A", (264,242)),
            "b": Button(pygame.K_b, "B", (412,175)),
            # "up": Button(pygame.K_UP),
            # "down": Button(pygame.K_DOWN),
            # "left": Button(pygame.K_LEFT),
            # "right": Button(pygame.K_RIGHT),
            "plus": Button(pygame.K_EQUALS, "plus", (314, 343)),
            "minus": Button(pygame.K_MINUS, "minus", (238,343)),
            "home": Button(pygame.K_h, "home", (276,343)),
            "1": Button(pygame.K_1, "1", (272,476)),
            "2": Button(pygame.K_2, "2", (272,530))
        }
        self.btnState = 0
        with open(f"{DIR}/config.json") as f:
            self.config = json.load(f)


    def run(self):
        while True:
            self.screen.fill((0,0,0))
            self.base_top.render(self.screen)
            self.base_bottom.render(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.btnState = event.key
                if event.type == pygame.KEYUP:
                    self.btnState = 0
            for btn in self.buttons:
                if self.btnState == self.buttons[btn].ID:
                    if self.buttons[btn].value == 0:
                        self.button_pressed(btn)
                elif self.buttons[btn].value == 1:
                    self.button_released(btn)
                if self.buttons[btn].holdtime != -1 and time.time() - self.buttons[btn].holdtime > 0.6:
                    self.button_held(btn)
                if self.buttons[btn].value == 1:
                    self.buttons[btn].image.render(self.screen)


            pygame.display.update()
                



    def button_pressed(self, btn):
        self.buttons[btn].value = 1
        self.buttons[btn].holdtime = time.time()


    def button_released(self, btn):
        self.buttons[btn].value = 0
        self.buttons[btn].holdtime = -1
        self.buttons[btn].holding = False


    def button_held(self, btn):
        self.buttons[btn].holdtime = -1
        self.buttons[btn].holding = True
        


if __name__ == "__main__":
    DevWiiid().run()

