import time
from os import environ
from tvdb_client import ApiV2Client
from time import gmtime, strftime
from operator import itemgetter
from sys import argv

from io_utlis import load_shows, parse_args, save_json
from constants import ENDED, SERIES_NAME, DOUBLE, TRIPLE, OUT_FILE

SHOWS = None
MISSING = []

api_client = ApiV2Client('nadinasiddiquiwaz', 'ZEDKTMYBNB29LBOS', 'EISRLGJH035SO60Q')
api_client.login()

DATE = int(strftime("%Y%m%d", gmtime()))


def main(args):

    global SHOWS
    SHOWS = load_shows(read_only=True)
    parse_args(args)
    load_all()
    save_json({'files': MISSING, 'info': 'No Missing Files'}, environ[OUT_FILE])


def load_all():
    for show in sorted(SHOWS.values(), key=get_series_name):
        if not show.status == ENDED and show.tvdb_id:
            check_for_newly_aired(show)
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


def check_for_newly_aired(show):
    episodes = []
    for i in range(1, 100):
        eps = api_client.get_series_episodes(show.tvdb_id, episode_number=None, page=i)
        if 'code' in eps:
            break
        episodes.extend(eps['data'])

    missing = []
    if not episodes:
        print(show.series_name)
        return
    episodes = sorted(episodes, key=itemgetter('airedSeason', 'airedEpisodeNumber'), reverse=True)
    for e in episodes:
        if e['airedSeason'] == 0:
            continue
        try:
            first_aired = int(''.join(e['firstAired'].split('-')))
        except:
            continue
        if first_aired >= DATE:
            continue
        if show.get_episode_by_sxe(s_nr=e['airedSeason'], e_nr=e['airedEpisodeNumber']):
            break
        missing.append({SERIES_NAME: show.series_name, 's_nr': e['airedSeason'], 'e_nr': e['airedEpisodeNumber']})

    if missing:
        for m in reversed(missing):
            MISSING.append({'key': len(MISSING), SERIES_NAME: m[SERIES_NAME], 's_nr': m['s_nr'], 'e_nr': m['e_nr']})

    pass


def get_series_name(show):
    return show.series_name


if __name__ == '__main__':
    start = time.time()
    main(argv[1:])
    print(time.time() - start)
