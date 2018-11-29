import io_utlis
from constants import *
import sys
import os

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows()
    io_utlis.parse_args(args)

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    update = prep_data(SHOWS)

    io_utlis.save_json(update, os.environ['OUTPUT_FILE'])
    io_utlis.save_shows(SHOWS)


def prep_data(shows):
    update = []
    for s in shows.keys():
        show = shows[s]
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
    main(sys.argv[1:])
