import io_utlis
import os
import unlock_shows
import time
import sys
from constants import *

SHOWS = None
MISSING = []

def load_tree():
    global SHOWS
    SHOWS = io_utlis.load_shows()
    if SHOWS is None:
        print('shows locked')
        return {'shows_locked': True}
    tree_file = {}
    tree_file['shows'] = load_all()
    io_utlis.save_shows(SHOWS)
    return tree_file

def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows()
    io_utlis.parse_args(args)
    conf = io_utlis.load_json(os.environ["CONF_FILE"])
    tree_file = io_utlis.load_json(os.environ['OUTPUT_FILE'])
    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    series_name = conf[SERIES_NAME]

    if series_name == '*':
        tree_file = {}
        tree_file['shows'] = load_all()
    else:
        show = SHOWS[series_name]
        tree_file['shows'][series_name] = get_show_data(show)
    for l in MISSING:
        print(l)
    io_utlis.save_json(tree_file, os.environ['OUTPUT_FILE'])
    io_utlis.save_shows(SHOWS)


def load_all():
    tree = {}
    for show in SHOWS.values():
        tree[show.series_name] = get_show_data(show)
    return tree


def get_show_data(show):
    seasons = []
    for season in show.seasons.values():
        sea = {'key': season.s_nr, 'episodes': [], 'opened': False}
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            sea['episodes'].append({LOCATION: episode.location,
                                    'file_name': episode.file_name,
                                    'e_nr': episode.e_nr,
                                    's_nr':episode.s_nr,
                                    'title': episode.title,
                                    'title2': episode.title2,
                                    'title3': episode.title3,
                                    'extension': episode.extension,
                                    'save': False,
                                    'delete': False,
                                    'episode_option': episode.episode_option,
                                    'size': episode.size,
                                    'duration': episode.duration,
                                    'quality': episode.quality,
                                    'tvdb_id': show.tvdb_id,
                                    'name_needed': show.name_needed})

        seasons.append(sea)
    return {SERIES_NAME: show.series_name, 'seasons': seasons}


def check_for_missing_season(show, s, seasons):
    index = seasons.index(s)
    if index <= 0:
        if s.s_nr <= 1:
            return
        for nr in range(1, s.s_nr):
            MISSING.append({SERIES_NAME: show.series_name, 's_nr': nr, 'e_nr': '*'})
    last = seasons[index-1]
    for nr in range(last.s_nr + 1, s.s_nr):
        MISSING.append({SERIES_NAME: show.series_name, 's_nr': nr, 'e_nr': '*'})


def check_for_missing_episode(show, e, episodes):
    if e.e_nr >= 777:
        return
    index = episodes.index(e)
    if index <= 0:
        if e.e_nr <= 1:
            return
        for nr in range(1, e.e_nr):
            MISSING.append({SERIES_NAME: show.series_name, 's_nr': e.s_nr, 'e_nr': nr})
    last = episodes[index-1]
    last_e_nr = last.e_nr
    if last.episode_option == DOUBLE:
        last_e_nr += 1
    elif last.episode_option == TRIPLE:
        last_e_nr += 2

    for nr in range(last_e_nr + 1, e.e_nr):
        MISSING.append({SERIES_NAME: show.series_name, 's_nr': e.s_nr, 'e_nr': nr})




def check_for_multiple_files(show, e):
    if show.series_name == 'Doctor Who Classic':
        return False
    if e.e_nr == 999:
        return False
    if e.e_nr < 777:
        return False



if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    print(time.time() - start)
