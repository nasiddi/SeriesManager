from utils.io_utlis import load_json, load_shows, parse_args, save_json
from utils.constants import EXCEPTIONS_FILE, CONF_FILE, OUT_FILE, NUMERALS, SINGLE, TRIPLE
from os import environ
from re import sub
from series import Series
from episode import Episode
from sys import argv
LOWER_GENERAL = load_json(EXCEPTIONS_FILE)['lower_general']


def generate_episode(e: Episode, title_nr, level):
    title = e.title
    if title_nr == 1 and e.title2:
        title = e.title2
    if title_nr == 2 and e.title3:
        title = e.title3
    title = remove_part(title)
    if title_nr > 0 and not title and e.title:
        title = e.title
        title = remove_part(title)
    title_low = title.lower()
    title_text = sub('[^A-Za-z0-9 ]+', '', title_low)
    if level == 'word':
        title_list = title_low.split(' ')
        title_text_list = title_text.split(' ')
    elif level == 'no_lows':
        title_list = title_low.split(' ')
        title_text_list = title_text.split(' ')
        for exception in LOWER_GENERAL:
            while exception in title_list:
                title_list.remove(exception)
            while exception in title_text_list:
                title_text_list.remove(exception)
    else:
        title_list = [title_low]
        title_text_list = [title_text]

    title_list.extend(title_text_list)
    title_list = list(set(title_list))
    return {
        's_nr': e.s_nr,
        'e_nr': e.e_nr + title_nr,
        'title': '',
        'solution': title,
        'title_list': title_list,
        'highlight': 'secondary'
    }


def remove_part(title):
    split = title.split(' ')
    if len(split) > 1 and split[-2] == 'Part' and split[-1] in NUMERALS:
        split = split[:-2]
    title = ' '.join(split)
    return title


def get_all_episodes(show, level):
    e_list = []
    total = 0
    for season in sorted(list(show.seasons.values()), key=lambda x: x.s_nr):
        s_list = []
        for ep in sorted(list(season.episodes.values()), key=lambda x: x.e_nr):
            s_list.append(generate_episode(ep, 0, level))
            total += 1
            if not ep.episode_option == SINGLE:
                s_list.append(generate_episode(ep, 1, level))
                total += 1
            if ep.episode_option == TRIPLE:
                s_list.append(generate_episode(ep, 2, level))
                total += 1

        e_list.append(s_list)
    return e_list, total


def main(args):
    parse_args(args)
    conf = load_json(environ[CONF_FILE])
    # conf = {'series_name': 'Lost', 'level': 'word'}
    shows = load_shows(read_only=True)
    show: Series = shows[conf['series_name']]
    episodes, total = get_all_episodes(show, conf['level'])
    for s in episodes:
        for e in s:
            print(e)
    save_json({'episodes': episodes, 'total': total}, environ[OUT_FILE])


if __name__ == '__main__':
    main(argv[1:])



