import getopt
import json
import pickle
import sys
from json import loads
from math import gcd
from os import path, environ, remove
from shlex import split
from shutil import rmtree
from subprocess import check_output
from sys import stderr
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
    with open(file, "wb") as f:
        pickle.dump(data, f)


def pickle_load(file):
    with open(file, "rb") as f:
        return pickle.load(f)


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


def find_video_metadata(file):
    cmd = "ffprobe -v quiet -print_format json -show_streams -show_format -i"
    args = split(cmd)
    args.append(file)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    try:
        ffprobe_output = check_output(args).decode('utf-8')
    except Exception as e:
        print(path.basename(file), file=stderr)
        print(e, file=stderr)
        return None
    ffprobe_output = loads(ffprobe_output)

    # prints all the metadata available:
    # import pprint
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(ffprobe_output)

    height = 0
    width = 0
    duration = 0
    size = 0
    ratio = ''
    # for example, find height and width
    video_stream = None
    for stream in ffprobe_output['streams']:
        if 'codec_type' in stream and stream['codec_type'] == 'video':
            video_stream = stream
            break
    try:
        height = video_stream['height']
    except:
        pass
    try:
        width = video_stream['width']
    except:
        pass
    try:
        duration = int(float(ffprobe_output['format']['duration']) / 60 * 100) / 100.0
    except:
        pass
    try:
        size = int(float(ffprobe_output['format']['size']) / 1024.0 / 1024.0 * 100) / 100.0
    except:
        pass
    try:
        ratio = video_stream['display_aspect_ratio']
    except:
        if not height == 0 and not width == 0:
            d = gcd(width, height)
            ratio = str(int(width/d)) + ':' + str(int(height/d))

    # print(os.path.basename(file))
    # print('height', height, 'pixel')
    # print('size:', size, 'MB')
    # print('duration', duration, 'minutes')
    # print('ratio', ratio)
    # print('*************************')
    return height, width, size, duration, ratio