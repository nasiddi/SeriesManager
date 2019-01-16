import time
import multiprocessing
from operator import itemgetter
from os import environ
from sys import argv
from time import gmtime, strftime

from tvdb_client import ApiV2Client

from utils.constants import SERIES_NAME, DOUBLE, TRIPLE, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json

api_client = ApiV2Client('nadinasiddiquiwaz', 'ZEDKTMYBNB29LBOS', 'EISRLGJH035SO60Q')
api_client.login()

DATE = int(strftime("%Y%m%d", gmtime()))


def main(args):
    shows = load_shows(read_only=True)
    parse_args(args)

    shows = sorted(shows.values(), key=get_series_name)
    p = multiprocessing.Pool(8)
    missing_files = p.map(get_show_data, shows)
    p.close()
    p.join()
    missing_files = [item for sublist in missing_files for item in sublist]
    for i in range(len(missing_files)):
        missing_files[i]['key'] = i

    save_json({'files': missing_files, 'info': 'No Missing Files'}, environ[OUT_FILE])


def get_show_data(show):
    missing_files = []
    if show.tvdb_id:
        missing_files.extend(check_for_newly_aired(show))
    for s in show.seasons.values():
        missing_files.extend(check_for_missing_season(show, s, sorted(show.seasons.values(), key=lambda x: x.s_nr)))
        episodes = sorted(list(s.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            missing_files.extend(check_for_missing_episode(show, episode, episodes))
    return missing_files


def check_for_missing_season(show, s, seasons):
    missing_files = []
    index = seasons.index(s)
    if index <= 0:
        if s.s_nr <= 1:
            return []
        missing_files.extend(
            [{'key': 0, SERIES_NAME: show.series_name, 's_nr': nr, 'e_nr': '*'}
             for nr in range(1, s.s_nr)])
    last = seasons[index-1]
    missing_files.extend(
        [{'key': 0, SERIES_NAME: show.series_name, 's_nr': nr, 'e_nr': '*'}
         for nr in range(last.s_nr + 1, s.s_nr)])
    return missing_files


def check_for_missing_episode(show, e, episodes):
    missing_files = []
    if e.e_nr >= 777:
        return []
    index = episodes.index(e)
    if index <= 0:
        if e.e_nr <= 1:
            return []
        missing_files.extend(
            [{'key': 0, SERIES_NAME: show.series_name, 's_nr': e.s_nr, 'e_nr': nr}
             for nr in range(1, e.e_nr)])
    last = episodes[index-1]
    last_e_nr = last.e_nr
    if last.episode_option == DOUBLE:
        last_e_nr += 1
    elif last.episode_option == TRIPLE:
        last_e_nr += 2
    missing_files.extend(
        [{'key': 0, SERIES_NAME: show.series_name, 's_nr': e.s_nr, 'e_nr': nr}
         for nr in range(last_e_nr + 1, e.e_nr)])
    return missing_files


def check_for_newly_aired(show):
    missing_files = []
    episodes = []
    for i in range(1, 100):
        eps = api_client.get_series_episodes(show.tvdb_id, episode_number=None, page=i)
        if 'code' in eps:
            break
        episodes.extend(eps['data'])

    missing = []
    missing_seasons = []
    if not episodes:
        print(show.series_name)
        return []
    episodes = sorted(episodes, key=itemgetter('airedSeason', 'airedEpisodeNumber'), reverse=True)
    for e in episodes:
        if e['airedSeason'] == 0:
            continue
        try:
            first_aired = int(''.join(e['firstAired'].split('-')))
        except ValueError:
            continue
        except KeyError:
            continue
        if first_aired >= DATE:
            continue
        if show.get_episode_by_sxe(s_nr=e['airedSeason'], e_nr=e['airedEpisodeNumber']):
            break
        if e['airedSeason'] - 1 in missing_seasons:
            continue
        if e['airedSeason'] > show.get_last_episode().s_nr + 1:
            missing.append({SERIES_NAME: show.series_name, 's_nr': e['airedSeason'] - 1, 'e_nr': '*'})
            missing_seasons.append(e['airedSeason'] - 1)
            continue
        if e['airedSeason'] in missing_seasons:
            continue
        if missing_seasons and e['airedSeason'] > show.get_last_episode().s_nr:
            missing.append({SERIES_NAME: show.series_name, 's_nr': e['airedSeason'], 'e_nr': '*'})
            missing_seasons.append(e['airedSeason'])
            continue
        missing.append({SERIES_NAME: show.series_name, 's_nr': e['airedSeason'], 'e_nr': e['airedEpisodeNumber']})

    if missing:
        missing_files.extend(
            [{'key': 0, SERIES_NAME: m[SERIES_NAME], 's_nr': m['s_nr'], 'e_nr': m['e_nr']}
             for m in reversed(missing)])

    return missing_files


def get_series_name(show):
    return show.series_name


if __name__ == '__main__':
    start = time.time()
    multiprocessing.freeze_support()
    main(argv[1:])
    print(time.time() - start)
