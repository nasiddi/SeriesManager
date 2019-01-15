from operator import itemgetter
from tvdb_client import ApiV2Client
from series import Series
from utils.constants import SERIES_NAME, DOUBLE, TRIPLE, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json, save_shows


SHOWS = load_shows()

for s in sorted(list(SHOWS.values()), key=lambda k: k.series_name.lower()):
    if s.genre1 == 'Anime':
        print(s)
        s.genre1 = 'Animation'
    if s.genre2 == 'Anime':
        s.genre2 = 'Animation'
        print(s)

save_shows(SHOWS)
