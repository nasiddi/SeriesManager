from utils.io_utlis import load_json, load_shows, parse_args, save_json
from utils.constants import EXCEPTIONS_FILE, CONF_FILE, OUT_FILE
from os import environ
from re import sub
from series import Series
from episode import Episode
from sys import argv
LOWER_GENERAL = load_json(EXCEPTIONS_FILE)['lower_general']


def generate_episode(e: Episode, level):
    title = e.get_title().lower()
    title_text = sub('[^A-Za-z0-9]+', '', title)
    if level == 'word':
        title_list = title.split(' ')
        title_text_list = title_text.split(' ')
    elif level == 'no_lows':
        title_list = title.split(' ')
        title_text_list = title_text.split(' ')
        for exception in LOWER_GENERAL:
            while exception in title_list:
                title_list.remove(exception)
            while exception in title_text_list:
                title_text_list.remove(exception)
    else:
        title_list = [title]
        title_text_list = [title_text]
    return {
        's_nr': e.s_nr,
        'e_nr': e.e_nr,
        'title': '',
        'solution': e.get_title(),
        'title_list': title_list,
        'title_text_list': title_text_list,
        'highlight': 'secondary'
    }


def get_all_episodes(show, level):
    e_list = []
    total = 0
    for season in sorted(list(show.seasons.values()), key=lambda x: x.s_nr):
        s_list = []
        for ep in sorted(list(season.episodes.values()), key=lambda x: x.e_nr):
            s_list.append(generate_episode(ep, level))
            total += 1
        e_list.append(s_list)
    return e_list, total


def main(args):
    parse_args(args)
    conf = load_json(environ[CONF_FILE])
    #conf = {'series_name': 'Class', 'level': 'word'}
    shows = load_shows(read_only=True)
    show: Series = shows[conf['series_name']]
    episodes, total = get_all_episodes(show, conf['level'])
    save_json({'episodes': episodes, 'total': total}, environ[OUT_FILE])


if __name__ == '__main__':
    main(argv[1:])



