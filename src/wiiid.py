import sys
import cwiid
from zero_hid import Keyboard, KeyCodes
import time
import json
import os
import pygame
from util import Image
from button import Button

from strhid import hid

pygame.init()

keyboard = Keyboard()

DIR = os.path.dirname(os.path.abspath(__file__))


class Wiiid:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((720,720))
        pygame.display.set_caption("WiiiD")

        if not self.connect():
            sys.exit()
        self.rumble()
        self.wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        self.buttons = {
            "a": Button(self, cwiid.BTN_A, "a"),
            "b": Button(self, cwiid.BTN_B, "b"),
            "up": Button(self, cwiid.BTN_UP, "up"),
            "down": Button(self, cwiid.BTN_DOWN, "down"),
            "left": Button(self, cwiid.BTN_LEFT, "left"),
            "right": Button(self, cwiid.BTN_RIGHT, "right"),
            "plus": Button(self, cwiid.BTN_PLUS, "plus"),
            "minus": Button(self, cwiid.BTN_MINUS, "minus"),
            "home": Button(self, cwiid.BTN_HOME, "home"),
            "1": Button(self, cwiid.BTN_1, "1"),
            "2": Button(self, cwiid.BTN_2, "2")
        }
        with open(f"{DIR}/config.json") as f:
            self.config = json.load(f)


    def run(self):
        while True:
            self.screen.fill((0,0,0))

            btnState = self.wii.state["buttons"]
            for btn in self.buttons:
                button = self.buttons[btn]
                state = button.state(btnState)
                if state != None:
                    self.act(*state)
                button.render(self.screen)

            time.sleep(0.01)

            pygame.display.update()


    def act(self, action, btn):
        btn = ",".join(btn)
        try:
            mod, key, release = self.config[action][btn]
            keyboard.press([hid[mod]], hid[key], release)
        except KeyError as e:
            pass


    def rumble(self, seconds:float=0.3):
        self.wii.rumble = 1
        time.sleep(seconds)
        self.wii.rumble = 0


    def connect(self):
        while True:
            try:
                self.wii = cwiid.Wiimote()
                break
            except RuntimeError:
                pass
        return True


if __name__ == "__main__":
    Wiiid().run()
