from os import sep, walk, path
from sys import exit, setrecursionlimit
from time import time

import backup
from series import Series
from utils.constants import META_FILE, STATUS, NAME_NEEDED, PREMIERE, FINAL, TVDB_ID, SERIES_DIR, ANIME_DIR
from utils.io_utlis import load_json, load_shows, save_shows

setrecursionlimit(10000)


def load_files(top):
    shows = {}
    len_top = len(top.split(sep))
    for root, dirs, _ in walk(top):

        for name in dirs:
            if root == top:
                shows[name] = Series(location=path.join(root, name), series_name=name)
                continue

            if 'Specials' in name or 'Specials' in root:
                continue

            show = path.basename(root)

            if len(root.split(sep)) - len_top > 1:
                continue

            season = shows[show].add_season(location=path.join(root, name))
            season.update_episodes()

    return shows


def add_metadata(shows):
    meta = load_json(META_FILE)
    for show in shows.values():
        if show.series_name not in meta:
            continue
        info = meta[show.series_name]
        show.status = info[STATUS]
        show.name_needed = info[NAME_NEEDED]
        show.premiere = info[PREMIERE]
        show.final = info[FINAL]
        if TVDB_ID not in info:
            info[TVDB_ID] = ''
        show.tvdb_id = info[TVDB_ID] if not info[TVDB_ID] == 0 else ''

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


def main():
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
    add_metadata(shows)
    save_shows(shows)

    print(time() - start)
    return shows


if __name__ == '__main__':
    main()
