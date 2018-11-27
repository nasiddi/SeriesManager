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
import unlock_shows
import syncer
import file_tree

SHOWS = None


def main(args):
    start = time.time()
    global SHOWS
    unlock_shows.main()
    io_utlis.parse_args(args)
    error = io_utlis.load_json(os.environ["CONF_FILE"])
    tree_file = io_utlis.load_json(os.environ['OUTPUT_FILE'])
    SHOWS = io_utlis.load_shows()

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    io_utlis.save_json(error, 'data/save_tree_conf.json')
    queue = syncer.QUEUE

    if error:
        series_name = load_show(error, tree_file, queue)
    else:
        series_name = load_all()

    save_queue(queue)
    report = []
    for file in queue:
        report.append(file.get_report())
    print(json.dumps(report, indent=4, sort_keys=True))
    io_utlis.save_shows(SHOWS)
    file_tree.main(series_name=series_name if not error else error['series_name'], out_file=os.environ['OUTPUT_FILE'])
    print(time.time() - start)


def load_show(error, tree_file, queue):
    if error['delete']:
        err = File(location=error['old_location'],
                   s_nr=error['s_nr'],
                   e_nr=error['e_nr'],
                   series_name=error['series_name'],
                   title=error['title'],
                   episode_option=error['episode_option'],
                   name_needed=error[NAME_NEEDED],
                   delete=True,
                   anime=SHOWS[error['series_name']].anime)
        queue.append(err)
    elif error['save']:
        err = File(location=error['old_location'],
                   s_nr=error['s_nr'],
                   e_nr=error['e_nr'],
                   s_nr_old=error['s_nr_old'],
                   e_nr_old=error['e_nr_old'],
                   series_name=error['series_name'],
                   title=error['title'],
                   episode_option=error['episode_option'],
                   name_needed=error[NAME_NEEDED],
                   anime=SHOWS[error['series_name']].anime)
        syncer.queue_episode(err)

    for s in tree_file['shows'][error['series_name']]['seasons']:
        for e in s['episodes']:
            if e['delete']:
                e = File(location=e['location'],
                         s_nr=e['s_nr'],
                         e_nr=e['e_nr'],
                         series_name=error['series_name'],
                         title=e['title'],
                         title2=e['title2'],
                         title3=e['title3'],
                         episode_option=e['episode_option'],
                         name_needed=e[NAME_NEEDED],
                         delete=True,
                         anime=SHOWS[error['series_name']].anime)
                queue.append(e)
            elif e['save']:
                e = File(location=e['location'],
                         s_nr=e['s_nr'],
                         e_nr=e['e_nr'],
                         s_nr_old=e['s_nr_old'],
                         e_nr_old=e['e_nr_old'],
                         series_name=error['series_name'],
                         title=e['title'],
                         title2=e['title2'],
                         title3=e['title3'],
                         episode_option=e['episode_option'],
                         name_needed=e[NAME_NEEDED],
                         anime=SHOWS[error['series_name']].anime)
                syncer.queue_episode(e)
    return error['series_name']


def load_all(tree_file, queue):
    update = tree_file['shows']
    series_names = update.keys()

    for n in series_names:
        show = update[n]
        for s in show['seasons']:
            for e in s['episodes']:
                if e['delete']:
                    e = File(location=e['location'],
                             s_nr=e['s_nr'],
                             e_nr=e['e_nr'],
                             series_name=n,
                             title=e['title'],
                             title2=e['title2'],
                             title3=e['title3'],
                             episode_option=e['episode_option'],
                             name_needed=e[NAME_NEEDED],
                             delete=True,
                             anime=SHOWS[n].anime)
                    queue.append(e)
                elif e['save']:
                    e = File(location=e['location'],
                             s_nr=e['s_nr'],
                             e_nr=e['e_nr'],
                             s_nr_old=e['s_nr_old'],
                             e_nr_old=e['e_nr_old'],
                             series_name=n,
                             title=e['title'],
                             title2=e['title2'],
                             title3=e['title3'],
                             episode_option=e['episode_option'],
                             name_needed=e[NAME_NEEDED],
                             anime=SHOWS[n].anime)
                    syncer.queue_episode(e)
    return '*'


def save_queue(queue):
    for file in queue:
        if file.delete:
            os.remove(file.location)
            SHOWS[file.series_name].seasons[file.s_nr].update_episodes()
        if syncer.file_exists(file, SHOWS) and not file.s_nr == file.s_nr_old and not file.e_nr == file.e_nr_old:
            continue
        try:
            shutil.move(file.location, file.new_location)
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
            if not file.e_nr == file.e_nr_old or not file.s_nr == file.s_nr_old:
                try:
                    del show.seasons[file.s_nr_old].episodes[file.e_nr_old]
                except:
                    pass
            episode = Episode(location=file.new_location,
                              episode_option=file.episode_option,
                              title=file.title,
                              title2=file.title2,
                              title3=file.title3,
                              s_nr=file.s_nr,
                              e_nr=file.e_nr)

            if show.add_episode(episode):
                file.report['info'].append('Season created')


if __name__ == '__main__':
    main(sys.argv[1:])
