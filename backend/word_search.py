from os import environ
from sys import argv

from utils.constants import DICT_FILE, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json, load_json

SHOWS = None
DICTIONARY = {}
NEW_DICT = []
WORDS = []
UNIQUE = {}
UNIQUE_TITLE = {}
UNIQUE_WORDS_IN_TITLE = {}
USED_ONCE = []


def main(args):
    global SHOWS, DICTIONARY
    SHOWS = load_shows(read_only=True)
    parse_args(args)

    DICTIONARY = load_json(DICT_FILE)
    load_all()
    new_dict = sorted(list(set(NEW_DICT)))
    if new_dict:
        save_json(new_dict, DICT_FILE)

    unique = sorted(UNIQUE.items(), key=sort_unique, reverse=True)
    unique_title = sorted(UNIQUE_TITLE.items(), key=sort_unique, reverse=True)
    unique_words_in_title = sorted(UNIQUE_WORDS_IN_TITLE.items(), key=sort_unique_words_in_title, reverse=True)
    print(unique)
    save_json({'words': WORDS, 'info': 'Dictionary is up to date'}, environ[OUT_FILE])


def load_all():
    for show in SHOWS.values():
        get_show_data(show)


def get_show_data(show):
    for season in show.seasons.values():
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for e in episodes:
            search_for_new_words(e)
            search_title(e)


def search_for_new_words(e):
    words = e.file_name.rsplit('.', 1)[0].split(' ')
    new_word = False
    title_list = []
    for i in range(len(words)):
        w = words[i]
        if w == '':
            continue

        if w in DICTIONARY:
                NEW_DICT.append(w)
                if w not in UNIQUE:
                    UNIQUE[w] = 1
                else:
                    UNIQUE[w] += 1

        else:
            if w not in UNIQUE:
                new_word = True
                UNIQUE[w] = 1
                title_list.append({'word': w,
                                   'key': w,
                                   'index': i,
                                   'add': True,
                                   'changed': False})
            else:
                UNIQUE[w] += 1
    if new_word:
        WORDS.append({'location': e.location,
                      'file': e.file_name,
                      'words': title_list})


def search_title(e):
    for t in filter(None, [e.title, e.title2, e.title3]):
        if t not in UNIQUE_TITLE:
            UNIQUE_TITLE[t] = 1
        else:
            UNIQUE_TITLE[t] += 1

    words = e.get_title().split(' ')
    for i in range(len(words)):
        w = words[i]
        if w == '':
            continue

        if w not in UNIQUE_WORDS_IN_TITLE:
            UNIQUE_WORDS_IN_TITLE[w] = 1
        else:
            UNIQUE_WORDS_IN_TITLE[w] += 1


def sort_unique(d: dict):
    return d[1]


def sort_unique_words_in_title(d: dict):
    if d[1] == 1:
        USED_ONCE.append(d[0])
    return d[1]


if __name__ == '__main__':
    main(argv[1:])
