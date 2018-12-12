import os
from utils.io_utlis import *
from utils.constants import *
import error_search
from os.path import join
from series import Series
from episode import Episode
from test import *
from shutil import move


d = 'assets/backup/20181211_142847'
j_list = []
for f in os.listdir(d):
    p = os.path.join(d, f)
    if 'json' in p:
        j = load_json(p)
        j_list.append({f: j})

print(j_list)
