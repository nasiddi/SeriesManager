from os import path, remove
from time import time, sleep

from utils.constants import LOCK_File


def main():
    if not path.exists(LOCK_File):
        return
    try:
        remove(LOCK_File)
    except:
        pass
    start = time()
    while path.exists(LOCK_File) and time() - start < 1000:
        sleep(1)


if __name__ == '__main__':
    main()
