import os
from constants import LOCK_File
import time


def main():
    if not os.path.exists(LOCK_File):
        return
    try:
        os.remove(LOCK_File)
    except:
        pass
    start = time.time()
    while os.path.exists(LOCK_File) and time.time() - start < 1000:
        time.sleep(1)


if __name__ == '__main__':
    main()
