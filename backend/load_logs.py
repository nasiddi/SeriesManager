from utils.constants import OUT_FILE, LOG_DIR
from sys import argv
from utils.io_utlis import parse_args, load_json, save_json
from os import listdir, environ, path


def main(args, out_file='data/load_logs.json'):
    if args:
        parse_args(args)
        out_file = environ[OUT_FILE]
    logs = [{'file': f[:-5], 'data': load_json(path.join(LOG_DIR, f)), 'opened': True}
            for f in listdir(LOG_DIR) if f.endswith('json')]

    print(logs)

    save_json(logs, out_file)


if __name__ == '__main__':
    main(argv[1:])
