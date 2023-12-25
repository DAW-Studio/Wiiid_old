import os, sys

def restart():
    os.execv(sys.argv[0], sys.argv)
