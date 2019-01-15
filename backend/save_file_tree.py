from json import dumps
from os import environ
from shutil import move
from sys import argv
import syncer
from utils.constants import EXCEPTIONS_FILE, SERIES_NAME, NAME_NEEDED, CONF_FILE, OUT_FILE
from utils.file import File
from utils.io_utlis import load_shows, parse_args, save_json, save_shows, load_json, wait_on_creation, recursive_delete
from unlock_shows import unlock
from series import Series
from episode import Episode

SHOWS = None
EXCEPTIONS = {}


def main(args):
    global SHOWS, EXCEPTIONS
    unlock()
    parse_args(args)
    data = load_json(environ[CONF_FILE])
    save_json(data, 'data/save_tree.json')
    SHOWS = load_shows()
    EXCEPTIONS = load_json(EXCEPTIONS_FILE)
    if 'title_match' not in EXCEPTIONS:
        EXCEPTIONS['title_match'] = []
    if SHOWS is None:
        save_json({'shows_locked': True}, environ[OUT_FILE])
        print('shows locked')
        return
    queue = syncer.QUEUE
    queue_errors(data['errors'], queue)
    load_all(data['shows'], queue)
    save_json(EXCEPTIONS, EXCEPTIONS_FILE)
    save_queue(queue)
    report = []
    for file in queue:
        report.append(file.get_report())
    print(dumps(report, indent=4, sort_keys=True))
    save_shows(SHOWS)

    import file_tree
    file_tree.main(out_file=environ[OUT_FILE])


def queue_errors(errors, queue):
    for error in errors:
        series_name = error[SERIES_NAME]
        if 'exception' in error and error['exception']:
            e_id = f'{series_name} {error["s_nr"]:02d}x{error["e_nr"]:0{3 if error["anime"] else 2}d}'
            if error['exception'] not in ['part', 'double', 'lower_general', 'title_match']:
                if e_id not in EXCEPTIONS[error['exception']]:
                    EXCEPTIONS[error['exception']][e_id] = []
                EXCEPTIONS[error['exception']][e_id].append(error['word'])
                EXCEPTIONS[error['exception']][e_id] = sorted(list(set(EXCEPTIONS[error['exception']][e_id])))
            elif error['exception'] == 'double':
                if series_name not in EXCEPTIONS[error['exception']]:
                    EXCEPTIONS[error['exception']][series_name] = []
                EXCEPTIONS[error['exception']][series_name].append(error['title'])
                EXCEPTIONS[error['exception']][series_name] = sorted(list(set(EXCEPTIONS[error['exception']][series_name])))
            elif error['exception'] == 'lower_general':
                EXCEPTIONS[error['exception']].append(error['word'])
                EXCEPTIONS[error['exception']] = sorted(list(set(EXCEPTIONS[error['exception']])))
            elif error['exception'] == 'title_match' and error['save']:
                EXCEPTIONS[error['exception']].append(e_id)
                EXCEPTIONS[error['exception']] = sorted(list(set(EXCEPTIONS[error['exception']])))
            else:
                EXCEPTIONS[error['exception']].append(e_id)
                EXCEPTIONS[error['exception']] = sorted(list(set(EXCEPTIONS[error['exception']])))
            continue

        if error['delete']:
            err = File(old_location=error['old_location'],
                       s_nr=error['s_nr'],
                       e_nr=error['e_nr'],
                       series_name=series_name,
                       title=error['title'],
                       episode_option=error['episode_option'],
                       name_needed=error[NAME_NEEDED],
                       delete=True,
                       anime=SHOWS[series_name].anime)
            queue.append(err)
        elif error['save']:
            err = File(old_location=error['old_location'],
                       s_nr=error['s_nr'],
                       e_nr=error['e_nr'],
                       s_nr_old=error['s_nr_old'],
                       e_nr_old=error['e_nr_old'],
                       series_name=series_name,
                       title=error['title'],
                       episode_option=error['episode_option'],
                       name_needed=error[NAME_NEEDED],
                       anime=SHOWS[series_name].anime)
            syncer.queue_episode(err)


def load_all(update, queue):
    series_names = update.keys()

    for n in series_names:
        show = update[n]
        for s in show['seasons']:
            for e in s['episodes']:
                if e['delete']:
                    e = File(old_location=e['location'],
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
                    print(e)


                    e = File(old_location=e['location'],
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


def save_queue(queue):
    print(len(queue))
    for file in queue:
        print(file.location)
        if file.delete:
            recursive_delete(file.old_location)
            try:
                SHOWS[file.series_name].seasons[file.s_nr].update_episodes(reload_metadata=False)
            except FileNotFoundError:
                del SHOWS[file.series_name].seasons[file.s_nr]
            continue
        if syncer.file_exists(file, SHOWS) and not file.s_nr == file.s_nr_old \
                and not file.e_nr == file.e_nr_old and not file.e_nr_old >= 999:
            continue
        try:
            if file.old_location == file.location:
                continue
            move(file.old_location, file.location)
        except Exception as e:
            print('rename', e)
            file.report['error'].append('Copy failed')
            continue
        if wait_on_creation(file.location):
            file.report['success'].append('Copy successful')
        else:
            file.report['error'].append('Copy failed')
            continue
        show: Series = SHOWS[file.series_name]
        if not file.s_nr == file.s_nr_old or not file.e_nr == file.e_nr_old:
            e: Episode = show.seasons[file.s_nr_old].episodes.pop(file.e_nr_old, None)
            e.set_location(file.location)
            show.add_episode(e)
        else:
            show.get_episode_by_sxe(file.s_nr, file.e_nr).set_location(file.location)


if __name__ == '__main__':
    main(argv[1:])
