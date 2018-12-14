import json
import os
import shutil
from sys import argv

from episode import Episode
from series import Series
from utils.constants import CONF_FILE, OUT_FILE, FILE_DIR, SERIES_NAME, MAC_OFFSET, SUBS, HD_Movies, \
    SUB_DIR, SD_MOVIES, SERIES_DIR, ANIME_DIR
from utils.file import File
from utils.io_utlis import load_shows, parse_args, save_json, save_shows, load_json, wait_on_creation, recursive_delete, wait_on_delete

QUEUE = []
SHOWS = None
CLEAN_UP = []


def main(args):
    global SHOWS
    parse_args(args)
    data = load_json(os.environ[CONF_FILE])
    save_json(data, 'data/syncer.json')
    SHOWS = load_shows()

    if SHOWS is None:
        save_json({'shows_locked': True}, os.environ[OUT_FILE])
        print('shows locked')
        return
    save_json(data, 'data/sync')
    files = []
    for f in data:

        f = File(old_location=os.path.join(FILE_DIR, f['location']),
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
    log = load_json(os.path.join(
        os.path.dirname(os.environ[OUT_FILE]), 'synclog'))
    if not log:
        log = []
    log.extend(report)
    save_json(report, os.environ[OUT_FILE])
    save_json(log, os.path.join(os.path.dirname(
        os.environ[OUT_FILE]), 'synclog'))
    print(json.dumps(report, indent=4, sort_keys=True))
    save_shows(SHOWS)


def sync_queue(queue=None):
    if not queue:
        queue = QUEUE
    for file in queue:
        if file.delete:
            if recursive_delete(os.sep.join(file.old_location.split(os.sep)[:3 + MAC_OFFSET])):
                file.report['info'].append('Delete successful')
            else:
                file.report['error'].append('Delete failed')
            continue
        if file.override:
            delete_file(file)
            try:
                e = SHOWS[file.series_name].get_episode_by_sxe(file.s_nr, file.e_nr)
                if e:
                    del SHOWS[file.series_name].seasons[file.s_nr].episodes[file.e_nr]
                    SHOWS[file.series_name].seasons[file.s_nr].episode_numbers.remove(file.e_nr)

            except KeyError:
                pass
            except ValueError:
                pass
        if file.type_option == 'Series' and file_exists(file, SHOWS):
            file.report['error'].append('File exists')
            continue
        try:
            shutil.move(file.old_location, file.location)
        except Exception as e:
            print('rename', e)
            file.report['error'].append('Copy failed')
            return
        if wait_on_creation(file.location):
            file.report['success'].append('Copy successful')
        else:
            file.report['error'].append('Copy failed')
        if file.type_option == 'Series' and file.extension not in SUBS:
            show = SHOWS[file.series_name]
            if not show.status == file.status:
                file.report['info'].append('Status changed to ' + file.status)
                show.status = file.status
            e = Episode(file.location)
            e.update_file_meta()
            if show.add_episode(e):
                file.report['info'].append('Season created')
        loc = os.sep.join(file.old_location.split(os.sep)[:3 + MAC_OFFSET])
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
            file.report['info'].append('No File to delete')
            return False
        except AttributeError:
            file.report['info'].append('No File to delete')
            return False
    else:
        folder = HD_Movies if file.type_option == 'HD' else 'SD'
        for name in os.listdir(folder):
            if name.rsplit('.', 1)[0] == file.title:
                location = os.path.join(folder, name)
                break

    if location is None:
        file.report['info'].append('No File to delete')
        return False
    try:
        os.remove(location)
    except OSError as e:
        file.report['error'].append('Delete failed')
        print(e)
        return
    if wait_on_delete(location):
        file.report['success'].append('Delete successful')
    else:
        file.report['error'].append('Delete failed')


def create_new_series(file):
    from tvdb_client import ApiV2Client
    api_client = ApiV2Client('nadinasiddiquiwaz', 'ZEDKTMYBNB29LBOS', 'EISRLGJH035SO60Q')
    api_client.login()
    show = api_client.get_series(file.tvdb_id)
    premiere = ''
    if 'data' in show:
        premiere = show['data']['firstAired']
    print(get_base_path(file))
    print(get_base_path(file).rsplit(os.sep, 1))
    base_path = get_base_path(file).rsplit(os.sep, 1)[0]
    SHOWS.update({file.series_name: Series(series_name=file.series_name, status=file.status, tvdb_id=file.tvdb_id,
                                           name_needed=file.name_needed, location=base_path, premiere=premiere)})
    file.report['info'].append('Series created')


def queue_episode(file):
    name = Episode.compile_file_name(None, file=file)

    base_path = get_base_path(file)
    file.location = os.path.join(base_path, name)

    if file.subs:
        for sub in file.subs:
            QUEUE.append(File(old_location=sub,
                              series_name=file.series_name,
                              location=os.path.join(
                                  SUB_DIR, '{}.{}'.format(name.rsplit('.', 1)[0], sub.rsplit('.', 1)[1]))))
    QUEUE.append(file)
    return QUEUE


def queue_movie(file):
    file.location = os.path.join(
        HD_Movies if file.type_option == 'HD' else SD_MOVIES, '{f.title}.{f.extension}'.format(f=file))
    QUEUE.append(file)


def get_base_path(file):
    base_path = os.path.join(ANIME_DIR if file.anime else SERIES_DIR,
                             file.series_name, 'Season {:02d}'.format(file.s_nr))
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    wait_on_creation(base_path)
    return base_path


def ignore_file(file):
    split_loc = file.old_location.split(os.sep)
    loc = os.sep.join(split_loc[:3 + MAC_OFFSET])
    if os.path.isdir(loc):
        new_loc = ' '.join([loc, '[ignore]'])
    else:
        split_loc = file.old_location.rsplit('.', 1)
        split_loc[0] = ' '.join([split_loc[0], '[ignore]'])
        new_loc = '.'.join(split_loc)
    print(loc)
    print(new_loc)
    os.rename(loc, new_loc)


if __name__ == '__main__':
    main(argv[1:])
