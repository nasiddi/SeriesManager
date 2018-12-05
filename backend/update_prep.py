from sys import argv
from os import environ

from io_utlis import load_shows, parse_args, save_json
from constants import SERIES_NAME, NAME_NEEDED, STATUS, PREMIERE, FINAL, TVDB_ID, OUT_FILE

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
                       'name_needed_unchanged': show.name_needed,
                       STATUS: show.status,
                       'status_unchanged': show.status,
                       PREMIERE: show.premiere,
                       'premiere_unchanged': show.premiere,
                       FINAL: show.final,
                       'final_unchanged': show.final,
                       TVDB_ID: show.tvdb_id,
                       'tvdb_id_unchanged': show.tvdb_id})
        update = sorted(update, key=lambda k: k['series_name_unchanged'].lower())

    return update


if __name__ == '__main__':
    main(argv[1:])
