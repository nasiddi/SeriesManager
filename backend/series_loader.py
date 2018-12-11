from os import sep, walk, path, environ
from sys import exit, setrecursionlimit, argv
from time import time
import multiprocessing

import backup
from episode import Episode
from series import Series
from utils.constants import META_FILE, STATUS, NAME_NEEDED, PREMIERE, FINAL, TVDB_ID, SERIES_DIR, ANIME_DIR, CONF_FILE, SERIES_NAME
from utils.io_utlis import load_json, load_shows, save_shows, parse_args
from unlock_shows import unlock

setrecursionlimit(10000)
META_DATA = load_json(META_FILE)


def load_files(top):
    shows = {}
    len_top = len(top.split(sep))
    for root, dirs, _ in walk(top):

        for name in dirs:
            if root == top:
                shows[name] = Series(location=path.join(root, name), series_name=name)
                continue

            show = path.basename(root)

            if len(root.split(sep)) - len_top > 1:
                continue
            if 'Special' in name:
                continue

            season = shows[show].add_season(location=path.join(root, name))
            season.update_episodes(reload_metadata=False)

    return shows


def reload_metadata(shows):
    start = time()
    p = multiprocessing.Pool(28)
    show_list = p.map(loop_parallel, shows.values())
    p.close()
    p.join()
    print('metadata', time() - start)
    shows = {}
    for s in show_list:
        shows[s.series_name] = s
    return shows


def loop_parallel(show):
    add_show_metadata(show)
    show.update_metadata()
    return show


def add_show_metadata(show):
    if show.series_name not in META_DATA:
        return
    info = META_DATA[show.series_name]
    show.status = info[STATUS]
    show.name_needed = info[NAME_NEEDED]
    show.premiere = info[PREMIERE]
    show.final = info[FINAL]
    if TVDB_ID not in info:
        info[TVDB_ID] = ''
    show.tvdb_id = info[TVDB_ID] if not info[TVDB_ID] == 0 else ''
    return info


def add_metadata(shows):
    for show in shows.values():
        info = add_show_metadata(show)
        e: Episode
        for season in show.seasons.values():
            for e in season.episodes.values():
                try:
                    file_meta = info['seasons'][str(e.s_nr)][str(e.e_nr)]
                    e.duration = file_meta['duration']
                    e.size = file_meta['size']
                    e.ratio = file_meta['ratio']
                    e.width = file_meta['width']
                    e.height = file_meta['height']
                    e.quality = file_meta['quality']
                except:
                    print('*load metadata*', e.location)
                    e.update_file_meta()
                if not e.quality:
                    e.update_file_meta()


def main(args):
    parse_args(args)
    unlock()
    config = load_json(environ[CONF_FILE])
    start = time()
    print('running', SERIES_DIR)
    if not backup.main():
        print('backup failed')
        exit(-2)
    else:
        print('backup successful')
    load_shows(reload=True)
    shows = load_files(SERIES_DIR)
    shows.update(load_files(ANIME_DIR))
    if config['reload_metadata']:
        shows = reload_metadata(shows)
    else:
        add_metadata(shows)
    save_shows(shows)

    print(time() - start)
    return shows


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main(argv[1:])
