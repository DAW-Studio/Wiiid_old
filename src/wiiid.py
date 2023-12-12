import sys
import cwiid
from zero_hid import Keyboard, KeyCodes
import time
import json
import os
import pygame

from strhid import hid

pygame.init()

keyboard = Keyboard()

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
        try:
            self.active_image = Image(f"{name}_active.png", pos)
        except:
            self.active_image = self.image

    def render(self, surface:pygame.Surface):
        if self.value == 1:
            self.active_image.render(surface)
        else:
            self.image.render(surface)


class Tilt:
    x: int
    z: int


class Wiiid:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((700,700),pygame.FULLSCREEN)
        pygame.display.set_caption("Wiiid")
        self.base_top = Image("base_top.png", (220,90))
        self.base_bottom = Image("base_bottom.png", (374,90))

        self.searching = Image("searching.png", (0,0))
        self.screen.fill((0,0,0))
        self.searching.render(self.screen)
        pygame.display.update()

        connected = False
        while True:
            if self.connect():
                connected = True
                break
        if connected:
            print("connected")
        else:
            sys.exit()
        time.sleep(1)
        self.rumble()
        self.wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        self.tilt = Tilt
        self.buttons = {
            "a": Button(cwiid.BTN_A, "A", (264,242)),
            "b": Button(cwiid.BTN_B, "B", (412,175)),
            # "up": Button(cwiid.BTN_UP),
            # "down": Button(cwiid.BTN_DOWN),
            "left": Button(cwiid.BTN_LEFT, "left", (254,147)),
            # "right": Button(cwiid.BTN_RIGHT),
            "plus": Button(cwiid.BTN_PLUS, "plus", (314, 343)),
            "minus": Button(cwiid.BTN_MINUS, "minus", (238,343)),
            "home": Button(cwiid.BTN_HOME, "minus", (238,343)),
            "1": Button(cwiid.BTN_1, "1", (272,476)),
            "2": Button(cwiid.BTN_2, "2", (272,530))
        }
        with open(f"{DIR}/config.json") as f:
            self.config = json.load(f)

        


    def run(self):
        while True:
            self.screen.fill((0,0,0))
            self.base_top.render(self.screen)
            self.base_bottom.render(self.screen)

            btnState = self.wii.state["buttons"]
            for btn in self.buttons:
                button = self.buttons[btn]
                if (btnState & button.ID):
                    if button.value == 0:
                        self.button_pressed(btn)
                elif button.value == 1:
                    self.button_released(btn)
                if button.holdtime != -1 and time.time() - button.holdtime > 0.6:
                    self.button_held(btn)

                button.render(self.screen)


            if self.buttons["home"].value == 1:
                accState = self.wii.state["acc"]
                self.tilting(accState)
            time.sleep(0.01)

            pygame.display.update()


    def button_pressed(self, btn):
        if btn == "home":
            accState = self.wii.state["acc"]
            self.tilt.z = accState[0]
            self.tilt.x = accState[1]
        self.buttons[btn].value = 1
        self.buttons[btn].holdtime = time.time()


    def button_released(self, btn):
        if not self.buttons[btn].holding:
            holdtap = False
            for hold in self.buttons:
                if self.buttons[hold].holding:
                    holdtap = True
                    self.act("hold+tap", [hold,btn])
            if not holdtap:
                self.act("tap", [btn])
        else:
            keyboard.release()
        self.buttons[btn].value = 0
        self.buttons[btn].holdtime = -1
        self.buttons[btn].holding = False


    def button_held(self, btn):
        self.act("hold", [btn])
        self.buttons[btn].holdtime = -1
        self.buttons[btn].holding = True


    def tilting(self, acc):
        z = acc[0]
        if z < self.tilt.z-5:
            self.act("tilt", ["-z"])
        elif z > self.tilt.z+5:
            self.act("tilt", ["+z"])


    def act(self, action, btn):
        btn = ",".join(btn)
        # display.lcd_clear()
        # display.lcd_display_string(f"{action} {btn}", 1)
        try:
            mod, key, release = self.config[action][btn]
            keyboard.press([hid[mod]], hid[key], release)
            # display.lcd_display_string(f"{mod} {key}", 2)
        except KeyError as e:
            # display.lcd_display_string("Not Mapped", 2)
            # print(e)
            pass


    def rumble(self, seconds:float=0.3):
        self.wii.rumble = 1
        time.sleep(seconds)
        self.wii.rumble = 0


    def connect(self):
        try:
            self.wii = cwiid.Wiimote()
            return True
        except RuntimeError:
            return False


if __name__ == "__main__":
    Wiiid().run()
