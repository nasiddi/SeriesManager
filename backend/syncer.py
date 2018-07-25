import io_utlis
import os
import sys
import shutil
from constants import *


def sync_series():
    pass


def main(args):
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["CONF_FILE"])
    print(data)
    io_utlis.save_json(data, 'sync')
    for file in data:
        if file['syncit'] == 'nosync':
            continue
        if file['type_option']['selected'] == 'Series' and file['series_name'] == 'Series Name':
            continue
        print(file)
        if file['type_option']['selected'] == 'HD' or file['type_option']['selected'] == 'SD':
            if not file['e_name']:
                continue
            sync_movie(file)
            continue
        if file['type_option']['selected'] == 'Series':
            sync_series(file)
            continue


def sync_series(file):
    pass


def sync_movie(file):
    print(file['location'])
    print(os.path.join(HD_Movies if file['type_option']['selected'] == 'HD' else SD_MOVIES, file['e_name']))
    #shutil.move(file['location'], os.path.join(HD_Movies if file['type_option']['selected'] == 'HD' else SD_MOVIES, file['e_name']))


if __name__ == '__main__':
    main(sys.argv[1:])
