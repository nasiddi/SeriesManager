import io_utlis
import os
import unlock_shows
import time
import sys
from constants import *

def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows()
    io_utlis.parse_args(args)
    conf = io_utlis.load_json(os.environ["CONF_FILE"])
    tree_file = io_utlis.load_json(os.environ['OUTPUT_FILE'])
    if SHOWS is None:
        io_utlis.save_json({'error': 'Shows locked'}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    unlock_shows.main()
    series_name = conf[SERIES_NAME]

    if series_name == '*':
        tree_file = {}
        tree_file['shows'] = load_all()
    else:
        show = SHOWS[series_name]
        tree_file['shows'][series_name] = get_show_data(show)

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
        for episode in season.episodes.values():
            sea['episodes'].append({LOCATION: episode.location,
                                    'file_name': episode.file_name,
                                    'path': False,
                                    'edit': False,
                                    'key': episode.e_nr})
        seasons.append(sea)
    return {SERIES_NAME: show.series_name, 'seasons': seasons}


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    print(time.time() - start)