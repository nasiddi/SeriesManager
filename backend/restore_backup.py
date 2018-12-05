import os
from sys import argv
from shutil import copyfile

from io_utlis import load_shows, parse_args, save_json, save_shows, load_json, wait_on_delete
from constants import BACKUP_DIR, ASSETS, OUT_FILE

SHOWS = None


def main(args):
    global SHOWS
    parse_args(args)
    SHOWS = load_shows()
    if SHOWS is None:
        save_json({'error': 'Shows locked'}, os.environ[OUT_FILE])
        print('shows locked')
        return
    date = load_json(os.environ["CONF_FILE"])['date']
    folder = os.path.join(BACKUP_DIR, date)
    file_list = os.listdir(ASSETS)
    for f in file_list:
        if 'lock' in f:
            continue
        file = os.path.join(ASSETS, f)
        if os.path.isfile(file):
            try:
                os.remove(file)
                wait_on_delete(file)
            except:
                pass
    file_list = os.listdir(folder)
    for f in file_list:
        try:
            copyfile(os.path.join(folder, f), os.path.join(ASSETS, f))
        except:
            pass

    save_shows(SHOWS)
    save_json({'done': True}, os.environ[OUT_FILE])


if __name__ == '__main__':
    main(argv[1:])
