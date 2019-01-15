from episode import Episode
from utils.constants import EXCEPTIONS_FILE, SERIES_NAME, ENDED, NUMERALS, WRONG_SYMBOLS, EXTENSIONS
from utils.io_utlis import load_json
from tvdb_client import ApiV2Client
from operator import itemgetter


EXCEPTIONS = load_json(EXCEPTIONS_FILE)
if 'title_match' not in EXCEPTIONS:
    EXCEPTIONS['title_match'] = []
NAMES = {}

api_client = ApiV2Client('nadinasiddiquiwaz', 'ZEDKTMYBNB29LBOS', 'EISRLGJH035SO60Q')
api_client.login()


def _generate_error(message, e, show,
                    title='',
                    e_nr=None,
                    s_nr='',
                    update=False,
                    delete=False,
                    word='',
                    exception_type='',
                    exception=''):
    if exception_type:
        e_id = e.id()
        if exception_type == 'double':
            e_id = show.series_name
        if e_id in EXCEPTIONS[exception_type]:
            if not word:
                return
            if word in EXCEPTIONS[exception_type][e_id]:
                return
    return {
        'message': message,
        'old_location': e.location,
        'title': title if title else e.get_title(),
        SERIES_NAME: show.series_name,
        'e_nr': e_nr if e_nr is not None else e.e_nr,
        's_nr': s_nr if s_nr else e.s_nr,
        's_nr_old': e.s_nr,
        'e_nr_old': e.e_nr,
        'save': update,
        'delete': delete,
        'extension': e.extension,
        'header': e.file_name,
        'tvdb_id': show.tvdb_id,
        'name_needed': show.name_needed,
        'episode_option': e.episode_option,
        'anime': show.anime,
        'word': word,
        'exception': exception
    }


def check_title_against_db(show):
    episodes = []
    if not show.tvdb_id:
        return
    for i in range(1, 100):
        eps = api_client.get_series_episodes(show.tvdb_id, episode_number=None, page=i)
        if 'code' in eps:
            break
        episodes.extend(eps['data'])

    if not episodes:
        return
    episodes = sorted(episodes, key=itemgetter('airedSeason', 'airedEpisodeNumber'))
    for e in episodes:
        ep = show.get_episode_by_sxe(e['airedSeason'], e['airedEpisodeNumber'])
        if not ep:
            continue
        if not ep.get_title() == e['episodeName']:
            return _generate_error(message='Title mismatch: ', e=e, show=show,
                                   title=e['episodeName'], exception_type='title_match', exception='title_match')


def check_words(show, e):
    words = e.get_title().split(' ')
    for i in range(len(words)):
        w = words[i]
        if w == '':
            continue
        if w[0].lower() + w[1:] in EXCEPTIONS['lower_general']:
            if i == 0 or words[i-1][-1] in ['-', '&', '.']:
                if w[0].islower():
                    words[i] = w.capitalize()
                    title = ' '.join(words)
                    return _generate_error(message='LowerCase Error: ' + w, e=e, show=show, word=w, title=title,
                                           exception_type='lower')
                else:
                    continue

            if w[0].isupper():
                words[i] = w[0].lower() + w[1:]
                title = ' '.join(words)
                return _generate_error(message='UpperCase Error: ' + w, e=e, show=show, word=w, title=title,
                                       exception_type='upper')
            continue
        if w[0].islower():
            words[i] = w.capitalize()
            title = ' '.join(words)
            return _generate_error(message='LowerCase Error: ' + w, e=e, show=show, word=w, title=title,
                                   exception_type='lower')
    return


def check_part_number(show, e):
    substring = None
    t = e.get_title().split('Part ')
    if len(t) == 0:
        return
    if len(t) == 2:
        prev_title = ''
        next_title = ''
        previous = show.get_previous(e)
        following = show.get_next(e)
        if previous:
            prev_title = previous.get_title()
        if following:
            next_title = following.get_title()
        if 'Part ' not in prev_title and 'Part ' not in next_title:
            if next_title or show.status == ENDED:
                return _generate_error(message='Unnecessary Part Number', e=e, show=show, exception_type='part')
        if ' ' in t[-1]:
            substring = t[-1].split(' ', 1)
            t[-1] = substring[0]
        if t[-1] in NUMERALS:
            return
        if t[-1].isdigit():
            t[-1] = NUMERALS[int(t[-1])]
            if substring:
                substring[0] = t[-1]
                t[-1] = ' '.join(substring)
            title = 'Part '.join(t)
            return _generate_error(message='Part Number Integer Error', e=e,
                                   show=show, title=title, exception_type='part')
        if len(set(t[-1])) == 1:
            t[-1] = NUMERALS[len(t[-1])]
            title = 'Part '.join(t)
            return _generate_error(message='Part Number Roman Error', e=e,
                                   show=show, title=title, exception_type='part')
        return _generate_error(message='Part Number Parse Error', e=e, show=show, exception_type='part')
    if len(t) > 2:
        return _generate_error(message='Unnecessary Part Numbers', e=e, show=show, exception_type='part')
    return


def check_for_spaces(show, e):
    if '  ' in e.get_title():
        title = e.get_title().replace('  ', ' ')
        return _generate_error(message='Double Space', e=e, show=show, title=title)
    name = e.file_name.rsplit('.', 1)
    if not name:
        return
    if name[0][-1] == ' ':
        title = e.get_title().strip()
        return _generate_error(message='Space Before Extension', e=e, show=show, title=title)
    return


def check_for_missing_title(show, e):
    if not show.name_needed:
        return
    if e.title and not e.title == ' ':
        return
    return _generate_error(message='Title Missing', e=e, show=show)


def check_symbols(show, e):
    if any(s in e.get_title() for s in WRONG_SYMBOLS):
        return _generate_error(message='Symbol Error', e=e, show=show)


def check_series_name_and_numbers(show, e):
    file_name = e.file_name
    if not file_name.startswith(show.series_name):
        return _generate_error(message='Series Name Error', e=e, show=show)
    file_name = file_name.replace(show.series_name + ' ', '')
    try:
        s_nr = int(file_name[:2])
    except ValueError:
        return _generate_error(message='Season Number Error', e=e, show=show)
    if not s_nr == e.s_nr:
        return _generate_error(message='Season Number Error', e=e, show=show)
    if e.e_nr >= 999:
        return _generate_error(message='Episode Number Error', e=e, show=show, e_nr='')
    return


def check_for_multiple_files(show, e):
    if show.series_name == 'Doctor Who Classic':
        return
    if 777 <= e.e_nr < 999:
        return _generate_error(message='Multiple Files', e=e, show=show, e_nr='')
    return


def check_against_compiled(show, e):
    if show.series_name == 'Doctor Who Classic':
        return
    if not e.file_name == e.compile_file_name():
        return _generate_error(message='Compilation Mismatch', e=e, show=show)
    return


def check_for_name_used_twice(show, e):
    title = e.get_title()
    if not title:
        return
    if show.series_name not in NAMES:
        NAMES[show.series_name] = [title]
        return

    if title in NAMES[show.series_name]:
        return _generate_error(message='Name Used Twice', e=e, show=show, exception_type='double', word=title)
    else:
        NAMES[show.series_name].append(title)
        return


def check_extension(show, e):
    if e.extension not in EXTENSIONS:
        print(e.file_name)
        if not e.extension:
            return _generate_error(message='Extension Missing', e=e, show=show)
        return _generate_error(message='No Video Extension', e=e, show=show)


def check_for_empty_season(show, s):
    if not s.episodes:
        return _generate_error(message='Empty Season', e=Episode(location=s.location, s_nr=s.s_nr, e_nr=1), show=show)
