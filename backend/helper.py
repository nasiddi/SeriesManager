from operator import itemgetter
from tvdb_client import ApiV2Client
from series import Series
from utils.constants import SERIES_NAME, DOUBLE, TRIPLE, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json

api_client = ApiV2Client('nadinasiddiquiwaz', 'ZEDKTMYBNB29LBOS', 'EISRLGJH035SO60Q')
api_client.login()

import sys

sys.stdout = open('data/names.txt', 'w')


def check_title(show: Series):
    episodes = []
    if not show.tvdb_id:
        return
    for i in range(1, 100):
        eps = api_client.get_series_episodes(show.tvdb_id, episode_number=None, page=i)
        if 'code' in eps:
            break
        episodes.extend(eps['data'])

    if not episodes:
        print(show.series_name)
        return []
    episodes = sorted(episodes, key=itemgetter('airedSeason', 'airedEpisodeNumber'))
    for e in episodes:
        ep = show.get_episode_by_sxe(e['airedSeason'], e['airedEpisodeNumber'])
        if not ep:
            continue
        if not ep.get_title() == e['episodeName']:
            print(ep)
            print(ep.get_title())
            print(e['episodeName'])


SHOWS = load_shows(read_only=True)

for s in sorted(list(SHOWS.values()), key=lambda k: k.series_name.lower()):
    check_title(s)
