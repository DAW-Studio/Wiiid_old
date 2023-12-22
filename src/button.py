import pygame
import time
from util import Image


class Button:
    def __init__(self, wiiid, ID:int, name:str, value:int=0, holdtime:float=-1):
        self.wiiid = wiiid
        self.buttons = wiiid.buttons
        self.ID = ID
        self.value = value
        self.holdtime = holdtime
        self.holding = False
        self.image = Image(f"{name}.png", (0,0))

    def state(self, btnState):
        if (btnState & self.ID):
            if self.value == 0:
                return self.pressed()
        elif self.value == 1:
            return self.released()
        if self.holdtime != -1 and time.time() - self.holdtime > 0.6:
            return self.held()
        return None

    def holdtap(self):
        for btn in self.buttons:
            if self.buttons[btn].holding:
                return btn
        return None

    def pressed(self):
        self.value = 1
        self.holdtime = time.time()

    def released(self):
        self.value = 0
        self.holdtime = -1
        if not self.holding:
            heldBtn = self.holdtap()
            if heldBtn != None:
                return ["hold+tap", [heldBtn,self]]
            else:
                return ["tap", [self]]
        else:
            self.holding = False
            return ["release", [self]]

    def held(self):
        self.holdtime = -1
        self.holding = True
        return ["hold", [self]]

    def render(self, surface:pygame.Surface):
        if self.value == 1:
            self.image.render(surface)
