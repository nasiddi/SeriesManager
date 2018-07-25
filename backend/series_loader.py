from constants import *
import os
import shutil
from series import Series
from episode import Episode
import time
import getopt
import sys
from io_utlis import *

sys.setrecursionlimit(10000)


def load_files(top):
    shows = {}
    for root, dirs, _ in os.walk(top):
        for name in dirs:
            if root == top:
                shows[name] = Series(location=os.path.join(root, name), series_name=name)
                continue

            if 'Specials' in name or 'Specials' in root:
                continue

            show = os.path.basename(root)
            shows[show].add_season(location=os.path.join(root, name))

    for show in shows.values():
        for season in show.seasons.values():
            episodes = {}
            files = os.listdir(season.location)
            for file in files:
                episode = Episode(location=os.path.join(season.location, file), s_nr=season.s_nr)
                episodes[episode.e_nr] = episode
            season.episodes = episodes
    return shows


def link_objects(obj, min_obj, max_obj, objs, obj_nr):
    if obj_nr > min_obj:
        n = 1
        while obj_nr - n not in objs and n > min_obj:
            n += 1
        if n > min_obj:
            obj.previous = objs[obj_nr - n]

    if obj_nr < max_obj:
        n = 1
        while obj_nr + n not in objs and n < max_obj:
            n += 1
        if n < max_obj:
            obj.next = objs[obj_nr + n]


def link_seasons_and_episodes(shows):
    for show in shows.values():
        keys_sn = show.seasons.keys()
        show.season_count = len(keys_sn)
        for season in show.seasons.values():
            link_objects(season, min(keys_sn), max(keys_sn), show.seasons, season.s_nr)

            keys_ep = season.episodes.keys()
            for episode in season.episodes.values():
                link_objects(episode, min(keys_ep), max(keys_ep), season.episodes, episode.e_nr)
            if max(keys_sn) == season.s_nr:
                show.last_ep = season.episodes[max(keys_ep)]


def add_metadata(shows):
    meta = load_json(META_FILE)
    for show in shows.values():
        info = meta[show.series_name]
        show.status = info[STATUS]
        show.name_needed = info[NAME_NEEDED]
        show.premiere = info[PREMIERE]
        show.final = info[FINAL]

        for season in show.seasons.values():
            s_names = {}
            for ep in season.episodes.values():
                s_names[str(ep.e_nr)] = ep.e_name
                if ep.double:
                    s_names[str(ep.e_nr + 1)] = ep.e_name2 if ep.e_name2 else '++double++'

            if str(season.s_nr) not in meta[show.series_name][EP_NAMES]:
                meta[show.series_name][EP_NAMES].update({str(season.s_nr): {}})
            meta[show.series_name][EP_NAMES][str(season.s_nr)].update(s_names)
        show.names = info[EP_NAMES]
    save_json(meta, META_FILE)



def main(args):
    start = time.time()
    print('running')
    if False:
        shows = load_files(SERIES_DIR)
        shows.update(load_files(ANIME_DIR))
        pickle_dump(shows, 'shows')
    else:
        shows = pickle_load('shows')
    link_seasons_and_episodes(shows)


    add_metadata(shows)

    print(time.time() - start)


    return shows


if __name__ == '__main__':
    main(sys.argv[1:])
