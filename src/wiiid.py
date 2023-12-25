import sys
import cwiid
from zero_hid import Keyboard, KeyCodes
import time
import json
import os
import pygame
from util import Image
from button import Button
from scenes.connect import ConnectScene
from scenes.main import MainScene
from shortcut_functions import functions

from strhid import hid

pygame.init()

keyboard = Keyboard()

DIR = os.path.dirname(os.path.abspath(__file__))

os.system(f"cd {DIR};git pull")


class Wiiid:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((720,720))
        pygame.display.set_caption("WiiiD")
        self.scene = ConnectScene(self.screen)
        self.scene.render()
        pygame.display.update()

        if not self.connect():
            sys.exit()
        self.mainScene = MainScene(self.screen)
        self.rumble()
        self.wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        self.buttons = {
            "a": Button(self, cwiid.BTN_A, "a"),
            "b": Button(self, cwiid.BTN_B, ""),
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
            self.mainScene.render()

            btnState = self.wii.state["buttons"]
            for btn in self.buttons:
                button = self.buttons[btn]
                state = button.state(btnState)
                if state != None:
                    self.act(*state)
                button.render(self.screen)

            time.sleep(0.01)

            pygame.display.update()


    def act(self, action, btns):
        btn = ",".join(btns)
        try:
            shortcut = self.config[action][btn]
            if shortcut["type"] == "standard":
                keyboard.press([hid[shortcut["mod"]]], hid[shortcut["key"]], shortcut["release"])
            elif shortcut["type"] == "cycle":
                key = shortcut["key"][shortcut["cycle"]]
                shortcut["cycle"] = shortcut["cycle"]+1 if shortcut["cycle"] != len(shortcut["key"]) else 0
                keyboard.press([hid[shortcut["mod"]]], hid[shortcut["key"]], shortcut["release"])
            elif shortcut["type"] == "function":
                functions[shortcut["func"]](*shortcut["args"])
        except KeyError as e:
            self.mainScene.log(e)


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
