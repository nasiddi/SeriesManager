from constants import *
import io_utlis
import sys
from time import gmtime, strftime
from shutil import copyfile

SHOWS = None


def main(args=''):
    global SHOWS
    SHOWS = io_utlis.load_shows()

    if SHOWS is None:
        if args:
            io_utlis.save_json({'error': 'Shows locked'}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return False

    if args:
        io_utlis.parse_args(args)

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
        io_utlis.recursive_delete(os.path.join(BACKUP_DIR, folder_list[0]))

    io_utlis.save_shows(SHOWS)
    if args:
        io_utlis.save_json({'done': True}, os.environ['OUTPUT_FILE'])
    return True


if __name__ == '__main__':
    main(sys.argv[1:])
