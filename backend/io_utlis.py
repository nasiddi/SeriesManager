import json
import pickle
import time
import getopt
import sys
from constants import *


def save_json(data_json, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_json, indent=4, sort_keys=True))


def load_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as json_data:
            j_data = json.load(json_data)
    except FileNotFoundError:
        return {}
    return j_data


def load_shows(reload=False):
    if os.path.exists(LOCK_File):
        return None
    lock = open(LOCK_File, 'w+')
    lock.close()
    if reload:
        return
    return pickle_load('shows')


def wait_on_creation(file_path):
    start = time.time()
    while not os.path.exists(file_path) and time.time() - start < 5:
        pass
    if os.path.exists(file_path):
        return True
    return False


def save_shows(shows):
    meta = {}
    for show in shows.keys():
        meta.update(shows[show].save())
    pickle_dump(shows, 'shows')
    save_json(meta, 'data/metadata.json')
    try:
        os.remove(LOCK_File)
    except:
        pass




def pickle_dump(data, name):
    pickle.dump(data, open(os.path.join('data', name + '.pkl'), 'wb'))


def pickle_load(name):
    return pickle.load(open(os.path.join('data', name + '.pkl'), 'rb'))


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
            if os.path.isabs(arg):
                os.environ['CONF_FILE'] = arg
            else:
                os.environ['CONF_FILE'] = os.path.join('configurations', arg)
        if opt in ('-o', '--output'):
            if os.path.isabs(arg):
                os.environ['OUTPUT_FILE'] = arg
            else:
                os.environ['OUTPUT_FILE'] = os.path.join('data', arg)
        if opt in ('-d', '--data'):
            if os.path.isabs(arg):
                os.environ['DATA_FILE'] = arg
            else:
                os.environ['DATA_FILE'] = os.path.join('data', arg)


"""
    infos = {}

    with open("C:\\Users\\nadina\\Documents\\code\\FileManager\\assets\\status.txt") as f:
        status = f.readlines()

    with open("C:\\Users\\nadina\\Documents\\code\\FileManager\\assets\\names.txt") as f:
        names = f.readlines()
        
    for line_s, line_n in zip(status, names):
        line_s = line_s.rstrip('\n')
        line_s = line_s.split(';')
        line_n = line_n.split('#')

        show = shows[line_s[0]]
        info = {show.series_name: {'Status': line_s[3], 'Premiere': line_s[1] if not line_s[1] == ' ' else '', 'Final': line_s[2] if not line_s[2] == ' ' else '', 'Name Needed': True if line_n[3] == 'Y' else False, 'Names': []}}
        infos.update(info)
    save_json(infos, 'meta.json')
"""