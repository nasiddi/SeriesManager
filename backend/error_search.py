from constants import *


def generate_error(message, e, show,
                   title='',
                   e_nr='',
                   s_nr='',
                   s_nr_old='',
                   e_nr_old='',
                   update=False,
                   delete=False,
                   ):
    return {
        'message': message,
        'old_location': e.location,
        'title': title if title else e.get_title(),
        'series_name': show.series_name,
        'e_nr': e_nr if e_nr else e.e_nr,
        's_nr': s_nr if s_nr else e.s_nr,
        's_nr_old': s_nr_old if s_nr_old else e.s_nr,
        'e_nr_old': e_nr_old if e_nr_old else e.e_nr,
        'save': update,
        'delete': delete,
        'extension': e.extension,
        'header': e.file_name,
        'tvdb_id': show.tvdb_id,
        'name_needed': show.name_needed,
        'episode_option': e.episode_option,
        'anime': show.anime
    }


def check_part_number(show, e):
    substring = None
    t = e.get_title().split('Part ')
    if len(t) == 0:
        return False
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
                return generate_error(message='Unnecessary Part Number', e=e, show=show)
        if ' ' in t[-1]:
            substring = t[-1].split(' ', 1)
            t[-1] = substring[0]
        if t[-1] in NUMERALS:
            return False
        if t[-1].isdigit():
            t[-1] = NUMERALS[int(t[-1])]
            if substring:
                substring[0] = t[-1]
                t[-1] = ' '.join(substring)
            title = 'Part '.join(t)
            return generate_error(message='Part Number Integer Error', e=e, show=show, title=title)
        if len(set(t[-1])) == 1:
            t[-1] = NUMERALS[len(t[-1])]
            title = 'Part '.join(t)
            return generate_error(message='Part Number Roman Error', e=e, show=show, title=title)
        return generate_error(message='Part Number Parse Error', e=e, show=show)
    if len(t) > 2:
        return generate_error(message='Unnecessary Part Numbers', e=e, show=show)
    return False


def check_for_spaces(show, e):
    if '  ' in e.get_title():
        title = e.get_title().replace(' f ', ' ')
        return generate_error(message='Double Space', e=e, show=show, title=title)
    name = e.file_name.rsplit('.', 1)
    if not name:
        return False
    if name[0][-1] == ' ':
        title = e.get_title().strip()
        return generate_error(message='Space Before Extension', e=e, show=show, title=title)
    return False


def check_for_multiple_files(show, e):
    if show.series_name == 'Doctor Who Classic':
        return False
    if e.e_nr == 999:
        return False
    if e.e_nr < 777:
        return False
