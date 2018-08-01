import io_utlis
import os
import sys
import shutil
from constants import *
from file import File
from series import Series
from episode import Episode
import time
import json
import re

SHOWS = None


def main(args):
    global SHOWS
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["DATA_FILE"])
    io_utlis.save_json(data, 'data/batch_match.json')
    SHOWS = io_utlis.load_shows()

    if SHOWS is None:
        # io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    file_list = []
    for u in data['units']:
        if not u['select']:
            continue
        location = os.path.join(FILE_DIR, u['text'])
        if os.path.isfile(location):
            file_list.append(File(location=location))
        else:
            for root, dirs, files in os.walk(location):
                for name in files:
                    extention = name.split('.')[-1].lower()
                    if extention in EXTENTIONS:
                        if 'sample' in name.lower():
                            continue
                        file_list.append((File(location=os.path.join(root, name))))
                    if extention in SUBS:
                        file_list.append((File(location=os.path.join(root, name))))

    for reg in data['regex']:
        if not reg['value']:
            continue
        pattern = re.compile(reg['value'])
        for file in file_list:
            match = re.findall(pattern, file.location)
            if match:
                file.s_nr = int(match[0][1:3])
                file.e_nr = int(match[0][4:])
    json = {'files': []}
    for f in file_list:
        json['files'].append({
            'location': f.location.split('\\', 2)[2],
            'title': '',
            'title2': '',
            'title3': '',
            's_nr': f.s_nr,
            'e_nr': f.e_nr,
            'episode_option': 'Single',
        })

    io_utlis.save_json(json, os.environ['OUTPUT_FILE'])






    io_utlis.save_shows(SHOWS)





if __name__ == '__main__':
    main(sys.argv[1:])

