from sys import argv
from os import path, listdir, makedirs, stat, system
import shutil
from time import sleep

from utils.io_utlis import load_json, save_json
from utils.constants import FILE_DIR, LOCAL_DIR, LOG_DIR


def main(args):
    log_path = path.join(LOG_DIR, 'download_transfer.json')
    log = load_json(log_path)
    if not log:
        log = {'files': {}, 'sizes': {}}

    def save_log():
        save_json(log, log_path)
        log2 = load_json(log_path)
        print(log2)

    while True:
        mount_drives()
        local_files = listdir(LOCAL_DIR)
        for file in local_files:
            if file not in log['files']:
                if file not in log['sizes'] or log['sizes'][file] != 'done':
                    current_size = get_size(path.join(LOCAL_DIR, file))
                    if file not in log['sizes'] or not current_size == log['sizes'][file]:
                        log['sizes'][file] = current_size
                        save_log()
                        continue
                    else:
                        del log['sizes'][file]
                        save_log()

                log['files'][file] = 'copying'
                save_log()
                if copytree(path.join(LOCAL_DIR, file), path.join(FILE_DIR, file)):
                    log['files'][file] = 'copied'
                else:
                    del log['files'][file]
                save_log()

        remote_files = listdir(FILE_DIR)
        delete = []
        for file in log['files'].keys():
            if log['files'][file] == 'delete':
                continue
            if file not in remote_files:
                log['files'][file] = 'delete'
                save_log()

            if file not in local_files:
                delete.append(file)
                save_log()

        for key in delete:
            del log['files'][key]
            save_log()

        sleep(1)


def copytree(src, dst):
    if path.isfile(src):
        if not path.exists(dst) or stat(src).st_mtime - stat(dst).st_mtime > 1:
            try:
                shutil.copy2(src, dst)
                return True
            except:
                return False
    else:
        if not path.exists(dst):
            makedirs(dst)
        for item in listdir(src):
            s = path.join(src, item)
            d = path.join(dst, item)
            copytree(s, d)

    return True


def get_size(file):
    total_size = 0
    if path.isfile(file):
        total_size += path.getsize(file)
    else:
        for item in listdir(file):
            total_size += get_size(path.join(file, item))
    return total_size


def mount_drive(folder):
    system("/usr/bin/osascript -e \"try\" -e \"mount volume \\\"smb://nadina:Sherlock69@Rocinante/" + folder + "\\\"\" -e \"end try\"")


def mount_drives():
    mount_drive('Video')
    mount_drive('Temp')


if __name__ == '__main__':
    main(argv[1:])
