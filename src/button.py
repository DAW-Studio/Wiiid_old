import pygame
import time
from util import Image


class Button:
    def __init__(self, wiiid, ID:int, name:str, value:int=0, holdtime:float=-1):
        self.wiiid = wiiid
        self.ID = ID
        self.name = name
        self.value = value
        self.holdtime = holdtime
        self.holding = False
        try:
            self.image = Image(f"buttons/{name}.png", (0,0))
        except:
            self.image = None

    def state(self, btnState):
        if (btnState & self.ID):
            if self.value == 0:
                return self.pressed()
        elif self.value == 1:
            return self.released()
        if self.holdtime != -1 and time.time() - self.holdtime > 0.5:
            return self.held()
        return None

    def holdtap(self):
        for btn in self.wiiid.buttons:
            if self.wiiid.buttons[btn].holding:
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
                return ["hold+tap", [heldBtn,self.name]]
            else:
                return ["tap", [self.name]]
        else:
            self.holding = False
            return ["release", [self.name]]

    def held(self):
        self.holdtime = -1
        self.holding = True
        return ["hold", [self.name]]

    def render(self, surface:pygame.Surface):
        if self.value == 1:
            if self.image != None: self.image.render(surface)
