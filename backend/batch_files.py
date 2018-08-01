from constants import *
import os
from file import File
import re
import io_utlis
import sys


def main(args):
    io_utlis.parse_args(args)
    units = []
    downloads = os.listdir(FILE_DIR)
    for dl in downloads:
        d = os.path.join(FILE_DIR, dl)
        if os.path.isfile(d):
            units.append({'text': dl, 'value': [], 'select': False})
            continue
        file_list = []
        for root, dirs, files in os.walk(d):
            for name in files:
                extention = name.split('.')[-1].lower()
                if extention in EXTENTIONS:
                    if 'sample' in name.lower():
                        continue
                    file_list.append(name)
                if extention in SUBS:
                    file_list.append(name)
        if file_list:
            units.append({'text': dl, 'value': file_list, 'select': False})

    reg = [
        {'text': 'A', 'value': 'S[0-9]{2}E[0-9]{2}'},
        {'text': 'B', 'value': 's[0-9]{2}e[0-9]{2}'},
        {'text': 'C', 'value': '[0-9]{2}X[0-9]{2}'},
        {'text': 'D', 'value': '[0-9]{2}x[0-9]{2}'},
        {'text': 'E', 'value': ''},
        {'text': 'F', 'value': ''},
    ]
    js = {'regex': reg, 'units': units}

    io_utlis.save_json(js, os.environ[OUT_FILE])


if __name__ == '__main__':
    main(sys.argv[1:])
