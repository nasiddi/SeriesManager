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
    global SHOWS
    unlock_shows.main()
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["CONF_FILE"])

    SHOWS = io_utlis.load_shows()

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    # io_utlis.save_json(data, 'data/save_tree.json')
    update = data['shows']
    series_names = update.keys()
    queue = syncer.QUEUE

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

    save_queue(queue)
    report = []
    for file in queue:
        report.append(file.get_report())
    print(json.dumps(report, indent=4, sort_keys=True))
    io_utlis.save_shows(SHOWS)


def save_queue(queue):
    for file in queue:
        if file.delete:
            os.remove(file.location)
            SHOWS[file.series_name].seasons[file.s_nr].update_episodes()
        if syncer.file_exists(file, SHOWS):
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