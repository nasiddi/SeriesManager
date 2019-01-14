from os import environ
from sys import argv

from utils.constants import SERIES_NAME, NAME_NEEDED, STATUS, PREMIERE, FINAL, TVDB_ID, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = load_shows(read_only=True)
    parse_args(args)
    update = prep_data()

    save_json(update, environ[OUT_FILE])


def prep_data():
    update = []
    for s in SHOWS.keys():
        show = SHOWS[s]
        update.append({SERIES_NAME: show.series_name,
                       'series_name_unchanged': show.series_name,
                       NAME_NEEDED: show.name_needed,
                       STATUS: show.status,
                       PREMIERE: show.premiere,
                       FINAL: show.final,
                       TVDB_ID: show.tvdb_id,
                       'genre1': show.genre1 if not show.genre1 == 'Anime' else 'Animation',
                       'genre2': show.genre2 if not show.genre2 == 'Anime' else 'Animation',
                       'changed': False})
        update = sorted(update, key=lambda k: k[SERIES_NAME].lower())

    return update


if __name__ == '__main__':
    main(argv[1:])
