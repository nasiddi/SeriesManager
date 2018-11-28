import io_utlis
import os
import unlock_shows
import time
import sys
from constants import *

SHOWS = None
MISSING = []

def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows()
    io_utlis.parse_args(args)
    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return

    load_all()

    for l in MISSING:
        print(l)
    io_utlis.save_json({'files': MISSING, 'info': 'No Missing Files'}, os.environ['OUTPUT_FILE'])
    io_utlis.save_shows(SHOWS)


def load_all():
    for show in SHOWS.values():
        get_show_data(show)


def get_show_data(show):
    for season in show.seasons.values():
        check_for_missing_season(show, season, sorted(show.seasons.values(), key=lambda x: x.s_nr))
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            check_for_missing_episode(show, episode, episodes)


def check_for_missing_season(show, s, seasons):
    index = seasons.index(s)
    if index <= 0:
        if s.s_nr <= 1:
            return
        for nr in range(1, s.s_nr):
            MISSING.append({'key': len(MISSING), SERIES_NAME: show.series_name, 's_nr': nr, 'e_nr': '*'})
    last = seasons[index-1]
    for nr in range(last.s_nr + 1, s.s_nr):
        MISSING.append({'key': len(MISSING), SERIES_NAME: show.series_name, 's_nr': nr, 'e_nr': '*'})


def check_for_missing_episode(show, e, episodes):
    if e.e_nr >= 777:
        return
    index = episodes.index(e)
    if index <= 0:
        if e.e_nr <= 1:
            return
        for nr in range(1, e.e_nr):
            MISSING.append({'key': len(MISSING), SERIES_NAME: show.series_name, 's_nr': e.s_nr, 'e_nr': nr})
    last = episodes[index-1]
    last_e_nr = last.e_nr
    if last.episode_option == DOUBLE:
        last_e_nr += 1
    elif last.episode_option == TRIPLE:
        last_e_nr += 2

    for nr in range(last_e_nr + 1, e.e_nr):
        MISSING.append({'key': len(MISSING), SERIES_NAME: show.series_name, 's_nr': e.s_nr, 'e_nr': nr})


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    print(time.time() - start)
