import io_utlis
from constants import *
import json
import sys
import os
import shutil
from series import Series
from file import File
from syncer import single_format, double_format, triple_format
from episode import Episode
import time

SHOWS = None
QUEUE = []
REPORT = {'error': [], 'info': [], 'success': [], 'summary': {'total': {'f': 0, 'e': 0}, 'subs': 0, 'seasons': {}}}
CLEAN_UP = []


def main(args):
    global SHOWS
    SHOWS = io_utlis.load_shows()
    io_utlis.parse_args(args)

    data = io_utlis.load_json(os.environ["CONF_FILE"])
    io_utlis.save_json(data, 'data/batch_sync.json')

    if SHOWS is None:
        io_utlis.save_json({'error': 'Shows locked'}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    start = time.time()
    show = prep(data)
    print('prep', time.time() - start)

    if show:
        start = time.time()
        sync_queue(show)
        print('sync', time.time() - start)
        start = time.time()
        update_summary()
        print('update', time.time() - start)
        start = time.time()
        clean_up()
        print('clean up', time.time() - start)
        start = time.time()
        SHOWS[show.series_name] = show
        print('save', time.time() - start)

    print(json.dumps(REPORT, indent=4, sort_keys=True))

    io_utlis.save_json(REPORT, os.environ['OUTPUT_FILE'])
    io_utlis.save_shows(SHOWS)


def update_summary():
    summary = REPORT['summary']
    REPORT['summary'] = {}
    REPORT['summary']['total'] = str(summary['total']['f']) + ' Files (' + str(summary['total']['e'])\
                                 + ' Episodes) copied'
    if summary['subs']:
        REPORT['summary']['subs'] = str(summary['subs']) + ' Subtitles copied'
    REPORT['summary']['seasons'] = {}
    for season in summary['seasons'].keys():
        REPORT['summary']['seasons'][str(season)] = 'Season ' + str(season) + ': ' + str(summary['seasons'][season]['f'])\
                                    + ' Files (' + str(summary['seasons'][season]['e']) + ' Episodes) copied'


def prep(data):
    base = create_location(data[SERIES_NAME], data['anime'])
    if not base:
        return False
    show = Series(
        series_name=data[SERIES_NAME],
        location=base,
        tvdb_id=data[TVDB_ID],
        premiere=data[PREMIERE],
        final=data[FINAL],
        status=data[STATUS],
        name_needed=data[NAME_NEEDED]
    )

    REPORT['info'].append('Series Name: ' + show.series_name)
    REPORT['info'].append('Status: ' + show.status)

    for f in data['files']:
        if not f['s_nr'] or not f['e_nr']:
            continue

        f = File(location=os.path.join(FILE_DIR, f['location']),
                 series_name=show.series_name,
                 s_nr=f['s_nr'],
                 e_nr=f['e_nr'],
                 title=f['title'],
                 title2=f['title2'],
                 title3=f['title3'],
                 episode_option=f['episode_option'],
                 subs=f['sub'],
                 anime=show.anime)

        folder = make_season_folder(f.s_nr, show.location)
        if not folder:
            return False

        if f.episode_option == 'Single':
            name = single_format(f)
        elif f.episode_option == 'Double':
            name = double_format(f)
        else:
            name = triple_format(f)
        if f.subs:
            f.new_location = os.path.join(SUB_DIR, name)
        else:
            f.new_location = os.path.join(folder, name)
        QUEUE.append(f)

    return show


def sync_queue(show):
    summary = REPORT['summary']['seasons']
    total = REPORT['summary']['total']
    for file in QUEUE:
        start = time.time()
        if os.path.exists(file.new_location):
            REPORT['error'].append('File already exists: ' + file.new_location)
            continue
        try:
            shutil.move(file.location, file.new_location)
        except Exception as e:
            print('rename', e)
            REPORT['error'].append('Copy failed: ' + file.new_location)
            continue
        if io_utlis.wait_on_creation(file.new_location):
            REPORT['success'].append('Copy successful: ' + file.new_location)
            if file.subs:
                REPORT['summary']['subs'] += 1
            else:
                if file.s_nr not in summary:
                    summary[file.s_nr] = {'f': 0, 'e': 0}
                summary[file.s_nr]['f'] += 1
                summary[file.s_nr]['e'] += 1
                total['f'] += 1
                total['e'] += 1

                if file.episode_option == DOUBLE:
                    total['e'] += 1
                    summary[file.s_nr]['e'] += 1
                if file.episode_option == TRIPLE:
                    total['e'] += 2
                    summary[file.s_nr]['e'] += 2
        else:
            REPORT['error'].append('Copy failed: ' + file.new_location)
        episode = Episode(location=file.new_location,
                          episode_option=file.episode_option,
                          title=file.title,
                          title2=file.title2 if not file.episode_option == SINGLE else '',
                          title3=file.title3 if file.episode_option == TRIPLE else '',
                          s_nr=file.s_nr,
                          e_nr=file.e_nr)

        if show.add_episode(episode):
            REPORT['info'].append('Season ' + str(file.s_nr) + ' created')
        loc = SEPERATOR.join(file.location.split(SEPERATOR)[:3 + MAC_OFFSET])
        if os.path.isdir(loc):
            if loc not in CLEAN_UP:
                CLEAN_UP.append(loc)
        print(time.time() - start, os.path.basename(file.new_location))


def clean_up():
    for loc in CLEAN_UP:
        shutil.rmtree(loc)


def make_season_folder(s_nr, show_loc):
    folder = os.path.join(show_loc, 'Season {:02d}'.format(s_nr))
    if not os.path.exists(folder):
        os.makedirs(folder)
        if io_utlis.wait_on_creation(folder):
            REPORT['summary'].update({s_nr: {'f': 0, 'e': 0}})
            return folder
        else:
            REPORT['error'].append('Season ' + str(s_nr) + ' folder not created')
            return ''
    else:
        return folder


def create_location(name, anime):
    base_path = os.path.join(ANIME_DIR if anime else SERIES_DIR, name)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        io_utlis.wait_on_creation(base_path)
        return base_path
    else:
        REPORT['error'].append('Series already exists')
        return ''


if __name__ == '__main__':
    main(sys.argv[1:])
