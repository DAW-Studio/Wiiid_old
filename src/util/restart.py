import os, sys

def restart():
    print(sys.argv[0])
    os.execv(sys.argv[0], sys.argv)
