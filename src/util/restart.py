import os, sys

def restart():
    os.execv("xinit", ["-e python3 ~/Wiiid/src/wiiid.py"])
