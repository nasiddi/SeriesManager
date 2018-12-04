from constants import *

SHOWS = None
DICTIONARY = {}
NEW_DICT = []
WORDS = []
MISSING = []


def main(args):
    io_utlis.parse_args(args)
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
    io_utlis.save_json(backups, os.environ[OUT_FILE])


def join_dir(f, b):
    return os.path.join(BACKUP_DIR, b, f)


if __name__ == '__main__':
    main(sys.argv[1:])
