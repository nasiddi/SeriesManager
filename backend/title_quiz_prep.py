from sys import argv
from os import environ
from utils.io_utlis import load_shows, parse_args, save_json
from utils.constants import OUT_FILE


def main(args):
    parse_args(args)
    shows = load_shows(read_only=True)
    names = list(shows.keys())
    save_json({'shows': names}, environ[OUT_FILE])


if __name__ == '__main__':
    main(argv[1:])
