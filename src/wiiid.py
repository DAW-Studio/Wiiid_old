import sys
import cwiid
from zero_hid import Keyboard, Mouse, KeyCodes
import time
import json
import os
import pygame
from util import Image
from button import Button
from tilt import Tilt
from scenes.connect import ConnectScene
from scenes.main import MainScene
from shortcut_functions import functions

from strhid import hid

pygame.init()

keyboard = Keyboard()
mouse = Mouse()

DIR = os.path.dirname(os.path.abspath(__file__))



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
        self.tilt = Tilt()
        with open(f"{DIR}/config.json") as f:
            self.config = json.load(f)


    def run(self):
        while True:
            self.screen.fill((0,0,0))
            self.mainScene.render()

            btnState = self.wii.state["buttons"]
            accState = self.wii.state["acc"]
            state = self.tilt.state(accState)
            self.act(*state)
            for btn in self.buttons:
                button = self.buttons[btn]
                state = button.state(btnState)
                if state != None:
                    self.act(*state)
                button.render(self.screen)

            time.sleep(0.01)

            pygame.display.update()


    def act(self, action, args):
        if action != "":
            arg = ",".join(args)
            try:
                shortcut = self.config[action][arg]
                if shortcut["device"] == "keyboard":
                    if shortcut["type"] == "standard":
                        keyboard.press([hid[shortcut["mod"]]], hid[shortcut["key"]], shortcut["release"])
                    elif shortcut["type"] == "cycle":
                        cycle = shortcut["cycle"]
                        key = shortcut["key"][cycle]
                        mod = shortcut["mod"][cycle]
                        shortcut["cycle"] = cycle+1 if cycle < len(shortcut["key"])-1 else 0
                        keyboard.press([hid[mod]], hid[key], shortcut["release"])
                elif shortcut["device"] == "mouse":
                    if shortcut["type"] == "click":
                        if shortcut["button"] == "left": mouse.left_click()
                        elif shortcut["button"] == "right": mouse.right_click()
                    if shortcut["type"] == "position_relative":
                        mouse.move_relative(shortcut["x"], shortcut["y"])
                elif shortcut["device"] == None:
                    if shortcut["type"] == "function":
                        functions[shortcut["func"]](*shortcut["args"])
            except Exception as e:
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
