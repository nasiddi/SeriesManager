import io_utlis
import os
import sys
import shutil
from constants import *
from file import File
from series import Series
from episode import Episode
import time
import json

QUEUE = []
SHOWS = None
CLEAN_UP = []


def main(args):
    global SHOWS
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["DATA_FILE"])

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
                 series_name=f['series_name'],
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
            CLEAN_UP.append(SEPERATOR.join(file.location.split(SEPERATOR)[:3 + MAC_OFFSET]))
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
            queue_episode(file)
            continue


    sync_queue()
    clean_up()
    report = []
    for file in QUEUE:
        report.append(file.get_report())
    io_utlis.save_json(report, os.environ['OUTPUT_FILE'])
    print(json.dumps(report, indent=4, sort_keys=True))
    io_utlis.save_shows(SHOWS)



def sync_queue():
    for file in QUEUE:
        if file.override:
            delete_file(file)
        if os.path.exists(file.new_location):
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
        if file.type_option == 'Series' and file.extention not in SUBS:
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


def clean_up():
    for loc in CLEAN_UP:
        if os.path.isdir(loc):
            shutil.rmtree(loc)
        else:
            os.remove(loc)


def delete_file(file):
    location = None
    if file.type_option == 'Series':
        try:
            location = SHOWS[file.series_name].get_episode_by_sxe(file.s_nr, file.e_nr).location
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
        file.report['success'].append('Delete successful')
    else:
        file.report['error'].append('Delete failed')


def create_new_series(file):
    basepath = get_basepath(file).rsplit(SEPERATOR, 1)[0 + MAC_OFFSET]
    SHOWS.update({file.series_name: Series(series_name=file.series_name, status=file.status, tvdb_id=file.tvdb_id,
                  anime=file.anime, name_needed=file.name_needed, location=basepath)})
    file.report['info'].append('Series created')


def queue_episode(file):
    file.anime = SHOWS[file.series_name].anime

    if file.episode_option == 'Single':
        name = single_format(file)
    elif file.episode_option == 'Double':
        name = double_format(file)
    else:
        name = triple_format(file)

    basepath = get_basepath(file)
    file.new_location = os.path.join(basepath, name)

    if file.subs:
        for sub in file.subs:
            QUEUE.append(File(location=sub,
                              series_name=file.series_name,
                              new_location=os.path.join(
                                  SUB_DIR, '{}.{}'.format(name.rsplit('.', 1)[0], sub.rsplit('.', 1)[1]))))
    QUEUE.append(file)


def queue_movie(file):
    file.new_location = os.path.join(HD_Movies if file.type_option == 'HD' else SD_MOVIES, '{f.title}.{f.extention}'.format(f=file))
    QUEUE.append(file)


def get_basepath(file):
    basepath = os.path.join(ANIME_DIR if file.anime else SERIES_DIR, file.series_name, 'Season {:02d}'.format(file.s_nr))
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    io_utlis.wait_on_creation(basepath)
    return basepath


def ignore_file(file):
    split_loc = file.location.split(SEPERATOR)
    loc0 = SEPERATOR.join(split_loc[:3 + MAC_OFFSET])
    loc1 = SEPERATOR.join(split_loc[3 + MAC_OFFSET:])
    print(file.location)
    print(loc0)
    print(loc1)
    if os.path.isdir(loc0):
        loc0 = ''.join([loc0, ' [ignore]'])
        new_loc = SEPERATOR.join([loc0, loc1])
        print(new_loc)



def single_format(file):
    if file.title == '':
        return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d}.{f.extention}'.format(f=file, p=3 if file.anime else 2)
    return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} - {f.title}.{f.extention}'.format(f=file, p=3 if file.anime else 2)


def double_format(file):
    if file.title == '' and file.title2 == '':
        return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d}.{f.extention}' \
            .format(f=file, p=3 if file.anime else 2)
    if not file.title == file.title2 and not (file.title == '' or file.title2 == ''):
        return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d} - {f.title} & {f.title2}.{f.extention}'\
               .format(f=file, p=3 if file.anime else 2)
    return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d} - {t}.{f.extention}' \
        .format(f=file, p=3 if file.anime else 2, t=file.title if not file.title == '' else file.title2)


def triple_format(file):
    # no title
    if file.title == '' and file.title2 == '' and file.title3 == '':
        return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d} & {f.s_nr:02d}x{f.e_nr3:0{p}d}.{f.extention}' \
            .format(f=file, p=3 if file.anime else 2)
    # all titles
    if not file.title == file.title2 and not file.title == file.title3 and not (file.title == '' or file.title2 == '' or file.title3 == ''):
        return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d} & {f.s_nr:02d}x{f.e_nr3:0{p}d} - {f.title} & {f.title2} & {f.title3}.{f.extention}'\
               .format(f=file, p=3 if file.anime else 2)
    title_set = list(filter(None, list({file.title, file.title2, file.title3})))
    # one title
    if len(title_set) == 1:
        return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d} & {f.s_nr:02d}x{f.e_nr3:0{p}d} - {t}.{f.extention}' \
            .format(f=file, p=3 if file.anime else 2, t=title_set[0])
    # two titles
    return '{f.series_name} {f.s_nr:02d}x{f.e_nr:0{p}d} & {f.s_nr:02d}x{f.e_nr2:0{p}d} & {f.s_nr:02d}x{f.e_nr3:0{p}d} - {t[0]} & {t[1]}.{f.extention}' \
        .format(f=file, p=3 if file.anime else 2, t=title_set)




if __name__ == '__main__':
    main(sys.argv[1:])
