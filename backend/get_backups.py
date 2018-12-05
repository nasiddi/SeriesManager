import os
from sys import argv

from io_utlis import parse_args, save_json
from constants import BACKUP_DIR, OUT_FILE

SHOWS = None
DICTIONARY = {}
NEW_DICT = []
WORDS = []
MISSING = []


def main(args):
    parse_args(args)
    backups_list = os.listdir(BACKUP_DIR)
    backups = {'backups': [], 'selected': ''}
    for b in backups_list:
        b_split = b.split('_')
        timestamp = f'{b_split[0]} {b_split[1][:2]}:{b_split[1][2:4]}:{b_split[1][4:]} '
        print(os.listdir(os.path.join(BACKUP_DIR, b)))
        backups['backups'].append({
            'value': b,
            'text': timestamp + str(int(sum(os.path.getsize(f) for f in
                                            [join_dir(d, b) for d in os.listdir(os.path.join(BACKUP_DIR, b))]
                                            if os.path.isfile(f)) / 1024)) + ' KB'})
        backups['selected'] = b
    save_json(backups, os.environ[OUT_FILE])


def join_dir(f, b):
    return os.path.join(BACKUP_DIR, b, f)


if __name__ == '__main__':
    main(argv[1:])
