import json
import os
import shutil
from sys import argv

from episode import Episode
from series import Series
from utils.constants import SERIES_NAME, TVDB_ID, PREMIERE, FINAL, STATUS, NAME_NEEDED, FILE_DIR, \
    SUB_DIR, SINGLE, DOUBLE, TRIPLE, MAC_OFFSET, ANIME_DIR, SERIES_DIR, OUT_FILE, CONF_FILE
from utils.file import File
from utils.io_utlis import load_shows, parse_args, save_json, save_shows, wait_on_creation, load_json

SHOWS = None
QUEUE = []
REPORT = {'error': [], 'info': [], 'success': [], 'summary': {'total': {'f': 0, 'e': 0}, 'subs': 0, 'seasons': {}}}
CLEAN_UP = []


def main(args):
    global SHOWS

    parse_args(args)

    data = load_json(os.environ[CONF_FILE])
    save_json(data, 'data/batch_sync.json')
    SHOWS = load_shows()
    if SHOWS is None:
        save_json({'error': 'Shows locked'}, os.environ[OUT_FILE])
        print('shows locked')
        return
    show = prep(data)

    if show:
        sync_queue(show)
        update_summary()
        clean_up()
        SHOWS[show.series_name] = show
    save_json(REPORT, os.environ[OUT_FILE])
    save_shows(SHOWS)
    return REPORT


def update_summary():
    summary = REPORT['summary']
    REPORT['summary'] = {}
    REPORT['summary']['total'] = str(summary['total']['f']) + ' Files (' + str(summary['total']['e']) \
                                                                         + ' Episodes) copied'
    if summary['subs']:
        REPORT['summary']['subs'] = str(summary['subs']) + ' Subtitles copied'
    REPORT['summary']['seasons'] = {}
    for season in summary['seasons'].keys():
        REPORT['summary']['seasons'][str(season)] = 'Season ' + str(season) + ': ' + \
                                                    str(summary['seasons'][season]['f']) + ' Files (' \
                                                    + str(summary['seasons'][season]['e']) + ' Episodes) copied'


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

        f = File(old_location=os.path.join(FILE_DIR, f['location']),
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

        name = Episode.compile_file_name(None, file=f)
        if f.subs:
            f.location = os.path.join(SUB_DIR, name)
        else:
            f.location = os.path.join(folder, name)
        QUEUE.append(f)

    return show


def sync_queue(show):
    summary = REPORT['summary']['seasons']
    total = REPORT['summary']['total']
    for file in QUEUE:
        if os.path.exists(file.location):
            REPORT['error'].append('File already exists: ' + file.location)
            continue
        try:
            shutil.move(file.old_location, file.location)
        except Exception as e:
            print('rename', e)
            REPORT['error'].append('Copy failed: ' + file.location)
            continue
        if wait_on_creation(file.location):
            REPORT['success'].append('Copy successful: ' + file.location)
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
            REPORT['error'].append('Copy failed: ' + file.location)
        e = Episode(location=file.location)
        if show.add_episode(e):
            REPORT['info'].append('Season ' + str(file.s_nr) + ' created')
        loc = os.sep.join(file.old_location.split(os.sep)[:3 + MAC_OFFSET])
        if os.path.isdir(loc):
            if loc not in CLEAN_UP:
                CLEAN_UP.append(loc)

        show.update_metadata()


def clean_up():
    for loc in CLEAN_UP:
        shutil.rmtree(loc)


def make_season_folder(s_nr, show_loc):
    folder = os.path.join(show_loc, 'Season {:02d}'.format(s_nr))
    if not os.path.exists(folder):
        os.makedirs(folder)
        if wait_on_creation(folder):
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
        wait_on_creation(base_path)
        return base_path
    else:
        REPORT['error'].append('Series already exists')
        return ''


if __name__ == '__main__':
    main(argv[1:])
