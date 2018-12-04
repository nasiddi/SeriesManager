import io_utlis
import time
import sys
from constants import *
import tvdbsimple as tvdb
from time import gmtime, strftime

SHOWS = None
MISSING = []

tvdb.KEYS.API_KEY = "B43FF87DE395DF56"

DATE = int(strftime("%Y%m%d", gmtime()))


def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows(read_only=True)
    io_utlis.parse_args(args)

    load_all()
    io_utlis.save_json({'files': MISSING, 'info': 'No Missing Files'}, os.environ['OUTPUT_FILE'])


def load_all():
    for show in SHOWS.values():
        if not show.status == ENDED:
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
    tvdb_show = tvdb.Series(show.tvdb_id)
    episodes = tvdb_show.Episodes.all()
    io_utlis.pickle_dump(episodes, 'pickle/' + show.series_name + '_episodes.pkl')
    missing = []
    for e in reversed(episodes):
        if e['airedSeason'] == 0:
            continue
        first_aired = int(''.join(e['firstAired'].split('-')))
        if first_aired >= DATE:
            continue
        if show.get_episode_by_sxe(s_nr=e['airedSeason'], e_nr=e['airedEpisodeNumber']):
            break
        missing.append({SERIES_NAME: show.series_name, 's_nr': e['airedSeason'], 'e_nr': e['airedEpisodeNumber']})

    if missing:
        for m in reversed(missing):
            MISSING.append({'key': len(MISSING), SERIES_NAME: m[SERIES_NAME], 's_nr': m['s_nr'], 'e_nr': m['e_nr']})

    pass


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    print(time.time() - start)
