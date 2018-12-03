import json
import shutil
import sys
import time

import io_utlis
from constants import *
from episode import Episode
from file import File
from io_utlis import recursive_delete
from series import Series

QUEUE = []
SHOWS = None
CLEAN_UP = []


def main(args):
    global SHOWS
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["CONF_FILE"])

    SHOWS = io_utlis.load_shows()

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    io_utlis.save_json(data, 'data/sync')
    files = []
    for f in data:

        f = File(location=os.path.join(FILE_DIR, f['location']),
                 sync=f['sync'],
                 s_nr=f['s_nr'],
                 e_nr=f['e_nr'],
                 series_name=f[SERIES_NAME],
                 title=f['title'],
                 title2=f['title2'],
                 title3=f['title3'],
                 episode_option=f['e_o']['s'],
                 override=f['override'],
                 delete=f['delete'],
                 subs=f['subs'],
                 type_option=f['t_o']['s'],
                 status=f['status_o']['s'],
                 new_series=f['new_series'],
                 name_needed=True if f['name_o']['s'] == 'Name required' else False,
                 tvdb_id=f['tvdb_id'] if not f['tvdb_id'] == 0 else 0,
                 anime=True if f['new_series'] and f['anime_o']['s'] == 'Anime: Yes' else False)

        if f.new_series:
            create_new_series(f)
        files.append(f)

    for file in files:
        if file.delete:
            QUEUE.append(file)
            continue
        if file.type_option == '[ignore]':
            ignore_file(file)
            continue
        if not file.sync:
            continue
        if file.type_option in ['HD', 'SD']:
            queue_movie(file)
            continue
        if file.type_option == 'Series':
            file.anime = SHOWS[file.series_name].anime
            queue_episode(file)
            continue

    sync_queue()
    clean_up()
    report = []
    for file in QUEUE:
        report.append(file.get_report())
    log = io_utlis.load_json(os.path.join(
        os.path.dirname(os.environ['OUTPUT_FILE']), 'synclog'))
    if not log:
        log = []
    print(log)
    log.extend(report)
    io_utlis.save_json(report, os.environ['OUTPUT_FILE'])
    io_utlis.save_json(log, os.path.join(os.path.dirname(
        os.environ['OUTPUT_FILE']), 'synclog'))
    print(json.dumps(report, indent=4, sort_keys=True))
    io_utlis.save_shows(SHOWS)


def sync_queue(queue=None):
    if not queue:
        queue = QUEUE
    for file in queue:
        if file.delete:
            if recursive_delete(SEPERATOR.join(file.location.split(SEPERATOR)[:3 + MAC_OFFSET])):
                file.report['info'].append('Delete successful')
            else:
                file.report['error'].append('Delete failed')
            continue
        if file.override:
            delete_file(file)
        if file_exists(file, SHOWS):
            file.report['error'].append('File exists')
            continue
        try:
            start = time.time()
            shutil.move(file.location, file.new_location)
            print(time.time() - start)
        except Exception as e:
            print('rename', e)
            file.report['error'].append('Copy failed')
            continue
        if io_utlis.wait_on_creation(file.new_location):
            file.report['success'].append('Copy successful')
        else:
            file.report['error'].append('Copy failed')
        if file.type_option == 'Series' and file.extension not in SUBS:
            show = SHOWS[file.series_name]
            if not show.status == file.status:
                file.report['info'].append('Status changed to ' + file.status)
            show.status = file.status
            episode = Episode(location=file.new_location,
                              episode_option=file.episode_option,
                              title=file.title,
                              title2=file.title2,
                              title3=file.title3,
                              s_nr=file.s_nr,
                              e_nr=file.e_nr)

            if show.add_episode(episode):
                file.report['info'].append('Season created')
        loc = SEPERATOR.join(file.location.split(SEPERATOR)[:3 + MAC_OFFSET])
        if os.path.isdir(loc):
            if loc not in CLEAN_UP:
                CLEAN_UP.append(loc)


def file_exists(file, shows):
    if shows[file.series_name].get_episode_by_sxe(file.s_nr, file.e_nr):
        if os.path.exists(shows[file.series_name].get_episode_by_sxe(file.s_nr, file.e_nr).location):
            return True
    return False


def clean_up():
    for loc in CLEAN_UP:
        recursive_delete(loc)


def delete_file(file):
    location = None
    if file.type_option == 'Series':
        try:
            location = SHOWS[file.series_name].get_episode_by_sxe(
                file.s_nr, file.e_nr).location
        except KeyError:
            file.report['error'].append('Delete failed')
            return
        except AttributeError:
            file.report['error'].append('Delete failed')
            return
    else:
        dir = HD_Movies if file.type_option == 'HD' else 'SD'
        for name in os.listdir(dir):
            if name.rsplit('.', 1)[0] == file.title:
                location = os.path.join(dir, name)
                break

    if location is None:
        file.report['error'].append('Delete failed')
        return
    try:
        os.remove(location)
    except OSError as e:
        file.report['error'].append('Delete failed')
        print(e)
        return
    if io_utlis.wait_on_creation:
        file.report['error'].append('Delete failed')
    else:
        file.report['success'].append('Delete successful')


def create_new_series(file):
    print(get_basepath(file))
    print(get_basepath(file).rsplit(SEPERATOR, 1))
    basepath = get_basepath(file).rsplit(SEPERATOR, 1)[0]
    SHOWS.update({file.series_name: Series(series_name=file.series_name, status=file.status, tvdb_id=file.tvdb_id,
                                           anime=file.anime, name_needed=file.name_needed, location=basepath)})
    file.report['info'].append('Series created')


def queue_episode(file):
    name = Episode.compile_file_name(file)

    basepath = get_basepath(file)
    file.new_location = os.path.join(basepath, name)

    if file.subs:
        for sub in file.subs:
            QUEUE.append(File(location=sub,
                              series_name=file.series_name,
                              new_location=os.path.join(
                                  SUB_DIR, '{}.{}'.format(name.rsplit('.', 1)[0], sub.rsplit('.', 1)[1]))))
    QUEUE.append(file)
    return QUEUE


def queue_movie(file):
    file.new_location = os.path.join(
        HD_Movies if file.type_option == 'HD' else SD_MOVIES, '{f.title}.{f.extension}'.format(f=file))
    QUEUE.append(file)


def get_basepath(file):
    basepath = os.path.join(ANIME_DIR if file.anime else SERIES_DIR,
                            file.series_name, 'Season {:02d}'.format(file.s_nr))
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    io_utlis.wait_on_creation(basepath)
    return basepath


def ignore_file(file):
    split_loc = file.location.split(SEPERATOR)
    loc = SEPERATOR.join(split_loc[:3 + MAC_OFFSET])
    if os.path.isdir(loc):
        new_loc = ' '.join([loc, '[ignore]'])
    else:
        split_loc = file.location.rsplit('.', 1)
        split_loc[0] = ' '.join([split_loc[0], '[ignore]'])
        new_loc = '.'.join(split_loc)
    print(loc)
    print(new_loc)
    os.rename(loc, new_loc)





if __name__ == '__main__':
    main(sys.argv[1:])
