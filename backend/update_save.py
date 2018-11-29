import io_utlis
from constants import *
import sys
import os
import shutil
import update_prep

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows()
    io_utlis.parse_args(args)

    data = io_utlis.load_json(os.environ["CONF_FILE"])
    io_utlis.save_json(data, 'data/update_save.json')

    if SHOWS is None:
        io_utlis.save_json({'error': 'Shows locked'}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    for s in data:
        show = SHOWS[s['series_name_unchanged']]

        if not s['name_needed_unchanged'] == s[NAME_NEEDED]:
            print(s['series_name_unchanged'], NAME_NEEDED, s['name_needed_unchanged'], s[NAME_NEEDED])
            show.name_needed = s[NAME_NEEDED]
        if not s['status_unchanged'] == s[STATUS]:
            print(s['series_name_unchanged'], STATUS, s['status_unchanged'], s[STATUS])
            show.status = s[STATUS]
        if not s['premiere_unchanged'] == s[PREMIERE]:
            print(s['series_name_unchanged'], PREMIERE, s['premiere_unchanged'], s[PREMIERE])
            show.premiere = s[PREMIERE]
        if not s['final_unchanged'] == s[FINAL]:
            print(s['series_name_unchanged'], FINAL, s['final_unchanged'], s[FINAL])
            show.final = s[FINAL]
        if not s['tvdb_id_unchanged'] == s[TVDB_ID]:
            print(s['series_name_unchanged'], TVDB_ID, s['tvdb_id_unchanged'], s[TVDB_ID])
            show.tvdb_id = s[TVDB_ID]
        if not s['series_name_unchanged'] == s[SERIES_NAME]:
            print(s['series_name_unchanged'], s[SERIES_NAME])
            update_location(show, s[SERIES_NAME])
            SHOWS.pop(s['series_name_unchanged'], None)
            show.series_name = s[SERIES_NAME]
            SHOWS[show.series_name] = show

    io_utlis.save_json(update_prep.prep_data(SHOWS), os.environ['OUTPUT_FILE'])
    io_utlis.save_shows(SHOWS)


def update_location(show, des):
    new_loc = show.location.replace(show.series_name, des, 1)
    shutil.move(show.location, new_loc)
    show.location = new_loc

    for season in show.seasons.values():
        season.location = season.location.replace(show.series_name, des, 1)
        for ep in season.episodes.values():
            ep.update_location(show.series_name, des)


if __name__ == '__main__':
    main(sys.argv[1:])
