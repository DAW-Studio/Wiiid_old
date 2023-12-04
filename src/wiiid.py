import cwiid
import drivers
import time
import json
import os

from strhid import hid

from zero_hid import Keyboard, KeyCodes
keyboard = Keyboard()

display = drivers.Lcd()

DIR = os.path.dirname(os.path.abspath(__file__))

class Button:
    def __init__(self, ID:int, value:int=0, holdtime:float=-1):
        self.ID = ID
        self.value = value
        self.holdtime = holdtime
        self.holding = False


class Wiiid:
    def __init__(self) -> None:
        display.lcd_display_string("Wiiid", 1)
        for i in range(5):
            display.lcd_display_string(f"Attempts: {i}", 2)
            if self.connect():
                break
        display.lcd_display_string("Connected  ", 2)
        time.sleep(1)
        self.rumble()
        self.wii.rpt_mode = cwiid.RPT_BTN
        self.buttons = {
            "a": Button(cwiid.BTN_A),
            "b": Button(cwiid.BTN_B),
            "up": Button(cwiid.BTN_UP),
            "down": Button(cwiid.BTN_DOWN),
            "left": Button(cwiid.BTN_LEFT),
            "right": Button(cwiid.BTN_RIGHT),
            "plus": Button(cwiid.BTN_PLUS),
            "minus": Button(cwiid.BTN_MINUS),
            "home": Button(cwiid.BTN_HOME),
            "1": Button(cwiid.BTN_1),
            "2": Button(cwiid.BTN_2)
        }
        with open(f"{DIR}/config.json") as f:
            self.config = json.load(f)


    def run(self):
        while True:
            btnState = self.wii.state["buttons"]
            for btn in self.buttons:
                if (btnState & self.buttons[btn].ID):
                    if self.buttons[btn].value == 0:
                        self.button_pressed(btn)
                elif self.buttons[btn].value == 1:
                    self.button_released(btn)


    def button_pressed(self, btn):
        self.buttons[btn].value = 1


    def button_released(self, btn):
        self.buttons[btn].value = 0
        self.act("tap", btn)


    def act(self, action, btn):
        display.lcd_clear()
        display.lcd_display_string(f"{action} {btn}", 1)
        try:
            mod, key, release = self.config[action][btn]
            keyboard.press([hid[mod]], hid[key], release)
            display.lcd_display_string(f"{mod} {key}", 2)
        except KeyError as e:
            display.lcd_display_string("Not Mapped", 2)
            print(e)


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
