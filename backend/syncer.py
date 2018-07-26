import io_utlis
import os
import sys
import shutil
from constants import *
from file import File

QUEUE = []


def sync_series():
    pass


def main(args):
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["CONF_FILE"])
    io_utlis.save_json(data, 'data/sync')
    files = []
    for f in data:
        if f['sync'] == 'nosync':
            continue

        files.append(File(location=f['location'],
                          s_nr=f['s_nr'],
                          e_nr=f['e_nr'],
                          series_name=f['series_name'],
                          title=f['title'],
                          title2=f['title2'],
                          title3=f['title3'],
                          episode_option=f['episode_option']['selected'],
                          override=f['override'],
                          subs=f['subs'],
                          type_option=f['type_option']['selected']))

    for file in files:
        if file.type_option in ['HD', 'SD']:
            queue_movie(file)
            continue
        if file.type_option == 'Series':
            sync_series(file)
            continue


def sync_series(file):
    pass


def queue_movie(file):
    print(file.location)
    file.new_location = os.path.join(HD_Movies if file.type_option == 'HD' else SD_MOVIES, file.title + file.extention)
    print(file.new_location)
    QUEUE.append(file)
    #shutil.move(file['location'], os.path.join(HD_Movies if file['type_option']['selected'] == 'HD' else SD_MOVIES, file['title']))


if __name__ == '__main__':
    main(sys.argv[1:])
