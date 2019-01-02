import os
from utils.io_utlis import *
from utils.constants import *
import error_search
from os.path import join
from series import Series
from episode import Episode
from shutil import move
from tvdb_client import ApiV2Client

from utils.constants import SERIES_NAME, DOUBLE, TRIPLE, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json

shows = load_shows(read_only=True)

api_client = ApiV2Client('nadinasiddiquiwaz', 'ZEDKTMYBNB29LBOS', 'EISRLGJH035SO60Q')
api_client.login()

for show in shows.values():
    if not show.tvdb_id:
        continue
    api = api_client.get_series(show.tvdb_id)
    api_name = api['data']['seriesName']
    if not show.series_name == api_name:
        print(show.series_name, api_name, show.tvdb_id)



