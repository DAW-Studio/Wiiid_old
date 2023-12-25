import os, sys

def restart():
    os.execv("xinit", sys.argv)
