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
            units.append({'text': dl, 'files': [], 'select': False})
            continue
        file_list = []
        for root, dirs, files in os.walk(d):
            for name in files:
                extension = name.split('.')[-1].lower()
                if extension in EXTENSIONS:
                    if 'sample' in name.lower():
                        continue
                    file_list.append(name)
                if extension in SUBS:
                    file_list.append(name)
        if file_list:
            units.append({'text': dl, 'files': file_list, 'select': False, 'opened': False})
    counter = 0
    regex = [
        {'key': counter, 'regex': 'S[0-9]{2}E[0-9]{2}', 'matches': [],
         's_start': '1', 's_end': '3', 'e_start': '4', 'e_end': '6', 'sxe': []},
        {'key': counter+1, 'regex': 's[0-9]{2}e[0-9]{2}', 'matches': [],
         's_start': '1', 's_end': '3', 'e_start': '4', 'e_end': '6', 'sxe': []}
    ]
    counter += 2
    while counter < 10:
        regex.append({'key': counter, 'regex': '', 'matches': [], 's_start': '', 's_end': '', 'e_start': '', 'e_end': '', 'sxe': []})
        counter += 1

    js = {'regex': regex, 'units': units}

    io_utlis.save_json(js, os.environ[OUT_FILE])


if __name__ == '__main__':
    main(sys.argv[1:])
