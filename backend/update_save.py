from os import environ
from shutil import move
from sys import argv

import update_prep
from utils.constants import NAME_NEEDED, STATUS, PREMIERE, FINAL, TVDB_ID, SERIES_NAME, CONF_FILE, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json, save_shows, load_json

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = load_shows()
    parse_args(args)

    data = load_json(environ[CONF_FILE])
    save_json(data, 'data/update_save.json')

    if SHOWS is None:
        save_json({'error': 'Shows locked'}, environ[OUT_FILE])
        print('shows locked')
        return
    for s in data:
        show = SHOWS[s['series_name_unchanged']]
        if s['changed']:
            show.name_needed = s[NAME_NEEDED]
            show.status = s[STATUS]
            show.premiere = s[PREMIERE]
            show.final = s[FINAL]
            show.tvdb_id = s[TVDB_ID]
        if not s['series_name_unchanged'] == s[SERIES_NAME]:
            update_location(show, s[SERIES_NAME])
            SHOWS.pop(s['series_name_unchanged'], None)
            show.series_name = s[SERIES_NAME]
            SHOWS[show.series_name] = show

    update_prep.SHOWS = SHOWS
    save_json(update_prep.prep_data(), environ[OUT_FILE])
    save_shows(SHOWS)


def update_location(show, des):
    new_loc = show.location.replace(show.series_name, des, 1)
    move(show.location, new_loc)
    show.location = new_loc

    for season in show.seasons.values():
        season.location = season.location.replace(show.series_name, des, 1)
        for ep in season.episodes.values():
            ep.update_location(show.series_name, des)


if __name__ == '__main__':
    main(argv[1:])
