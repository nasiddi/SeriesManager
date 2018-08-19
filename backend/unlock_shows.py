import os
from constants import LOCK_File


def main():
    try:
        os.remove(LOCK_File)
    except:
        pass


if __name__ == '__main__':
    main()
