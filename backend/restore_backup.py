from constants import *
from shutil import copyfile

SHOWS = None


def main(args):
    global SHOWS
    io_utlis.parse_args(args)
    SHOWS = io_utlis.load_shows()
    if SHOWS is None:
        io_utlis.save_json({'error': 'Shows locked'}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    date = io_utlis.load_json(os.environ["CONF_FILE"])['date']
    folder = os.path.join(BACKUP_DIR, date)
    file_list = os.listdir(ASSETS)
    for f in file_list:
        if 'lock' in f:
            continue
        file = os.path.join(ASSETS, f)
        if os.path.isfile(file):
            try:
                os.remove(file)
                io_utlis.wait_on_delete(file)
            except:
                pass
    file_list = os.listdir(folder)
    for f in file_list:
        try:
            copyfile(os.path.join(folder, f), os.path.join(ASSETS, f))
        except:
            pass

    io_utlis.save_shows(SHOWS)
    io_utlis.save_json({'done': True}, os.environ['OUTPUT_FILE'])


if __name__ == '__main__':
    main(sys.argv[1:])
