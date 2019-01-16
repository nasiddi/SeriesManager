import os
from sys import argv

from utils.constants import BACKUP_DIR, OUT_FILE, ASSETS
from utils.io_utlis import parse_args, save_json, load_json

SHOWS = None
DICTIONARY = {}
NEW_DICT = []
WORDS = []
MISSING = []


def main(args):
    parse_args(args)
    backups_list = os.listdir(BACKUP_DIR)
    backups = {'backups': {}, 'selected': ''}
    for b in backups_list:
        b_split = b.split('_')
        timestamp = f'{b_split[0]} {b_split[1][:2]}:{b_split[1][2:4]}:{b_split[1][4:]} '
        folder = os.path.join(BACKUP_DIR, b)
        j_list = load_json_files(folder)
        backups['backups'][b] = {
            'key': b, 'content': j_list,
            'text': (timestamp + str(int(sum(os.path.getsize(f) for f in
                                             [os.path.join(BACKUP_DIR, b, d)
                                              for d in os.listdir(os.path.join(BACKUP_DIR, b))]
                                             if os.path.isfile(f) and 'test' not in f) / 1024)) + ' KB')}
        backups['selected'] = b
    current_files = load_json_files(ASSETS)
    backups['current'] = {'size': str(int(sum(os.path.getsize(f) for f in
                                              [os.path.join(ASSETS, d) for d in os.listdir(ASSETS)]
                                              if os.path.isfile(f) and 'test' not in f) / 1024)) + ' KB',
                          'content': current_files}
    save_json(backups, os.environ[OUT_FILE])


def load_json_files(folder):
    j_list = []
    for f in os.listdir(folder):
        p = os.path.join(folder, f)
        if 'json' in p and 'test' not in p:
            j = load_json(p)
            if type(j) is dict:
                j = dict(sorted(j.items())[:10])
            else:
                j = j[:10]
            j_list.append({'key': f, 'data': j, 'opened': True})
    return j_list


if __name__ == '__main__':
    main(argv[1:])
