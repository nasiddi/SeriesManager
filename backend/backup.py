import os
from shutil import copyfile
from sys import argv
from time import gmtime, strftime
from unlock_shows import unlock
from utils.constants import BACKUP_DIR, ASSETS, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json, recursive_delete

SHOWS = None


def main(args=''):
    global SHOWS
    SHOWS = load_shows()

    if SHOWS is None:
        if args:
            save_json({'error': 'Shows locked'}, os.environ[OUT_FILE])
        print('shows locked')
        return False

    if args:
        parse_args(args)

    date = strftime("%Y%m%d_%H%M%S", gmtime())
    print(date)
    folder = os.path.join(BACKUP_DIR, date)
    os.makedirs(folder)
    file_list = os.listdir(ASSETS)
    for f in file_list:
        if 'lock' in f:
            continue
        file = os.path.join(ASSETS, f)
        if os.path.isfile(file):
            try:
                copyfile(file, os.path.join(folder, f))
            except:
                pass

    folder_list = sorted(os.listdir(BACKUP_DIR))
    if len(folder_list) > 10:
        recursive_delete(os.path.join(BACKUP_DIR, folder_list[0]))

    unlock()
    if args:
        save_json({'done': True}, os.environ[OUT_FILE])
    return date


if __name__ == '__main__':
    main(argv[1:])
