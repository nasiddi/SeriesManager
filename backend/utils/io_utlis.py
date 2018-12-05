import getopt
import json
import pickle
import sys
from os import path, environ, remove
from shutil import rmtree
from time import time

from utils.constants import LOCK_File, SHOWS_FILE, META_FILE, OUT_FILE, CONF_FILE


def save_json(data_json, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_json, indent=4, sort_keys=True, ))


def load_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as json_data:
            j_data = json.load(json_data)
    except FileNotFoundError:
        return {}
    return j_data


def load_shows(reload=False, read_only=False):
    if path.exists(LOCK_File) and not read_only:
        return None
    if not read_only:
        lock = open(LOCK_File, 'w+')
        lock.close()
    if reload:
        return
    return pickle_load(SHOWS_FILE)


def wait_on_creation(file_path):
    start = time()
    while not path.exists(file_path) and time() - start < 5:
        pass
    if path.exists(file_path):
        return True
    return False


def wait_on_delete(file_path):
    start = time()
    while path.exists(file_path) and time() - start < 5:
        pass
    if not path.exists(file_path):
        return True
    return False


def save_shows(shows):
    meta = {}
    for show in shows.keys():
        meta.update(shows[show].save())
    pickle_dump(shows, SHOWS_FILE)
    save_json(meta, META_FILE)
    try:
        remove(LOCK_File)
    except:
        pass
    wait_on_delete(LOCK_File)


def pickle_dump(data, file):
    pickle.dump(data, open(file, 'wb'))


def pickle_load(file):
    return pickle.load(open(file, 'rb'))


def parse_args(args):
    try:
        opts, args = getopt.getopt(args, 'c:o:d:e:r:', ['config=', 'output=', 'data=', 'test=', 'train='])
    except getopt.GetoptError:
        print('usage: -c config.json -o output.json -d data.csv -e test.csv -r train.tsv')
        sys.exit(2)
    for opt, arg in opts:
        if not arg:
            continue
        if opt in ('-c', '--config'):
            if path.isabs(arg):
                environ[CONF_FILE] = arg
            else:
                environ[CONF_FILE] = path.join('configurations', arg)
        if opt in ('-o', '--output'):
            if path.isabs(arg):
                environ[OUT_FILE] = arg
            else:
                environ[OUT_FILE] = path.join('data', arg)
        if opt in ('-d', '--data'):
            if path.isabs(arg):
                environ['DATA_FILE'] = arg
            else:
                environ['DATA_FILE'] = path.join('data', arg)


def recursive_delete(location):
    if path.isdir(location):
        rmtree(location)
    else:
        remove(location)

    if path.exists(location):
        return False
    return True
