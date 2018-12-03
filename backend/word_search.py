import io_utlis
import time
import sys
from constants import *

SHOWS = None
DICTIONARY = {}
NEW_DICT = []
WORDS = []
MISSING = []


def main(args):
    global SHOWS, DICTIONARY
    SHOWS = io_utlis.load_shows(read_only=True)
    io_utlis.parse_args(args)

    DICTIONARY = io_utlis.load_json(DICT_FILE)
    load_all()
    new_dict = sorted(list(set(NEW_DICT)))
    io_utlis.save_json(new_dict, DICT_FILE)

    io_utlis.save_json({'words': WORDS, 'info': 'Dictionary is up to date'}, os.environ['OUTPUT_FILE'])


def load_all():
    for show in SHOWS.values():
        get_show_data(show)


def get_show_data(show):
    for season in show.seasons.values():
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for e in episodes:
            search_for_new_words(e)


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

        else:
            if w not in MISSING:
                new_word = True
                MISSING.append(w)
                title_list.append({'word': w,
                                   'key': w,
                                   'index': i,
                                   'add': True,
                                   'changed': False})
    if new_word:
        WORDS.append({'location': e.location,
                      'file': e.file_name,
                      'words': title_list})


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    print(time.time() - start)


if __name__ == '__main__':
    main(sys.argv[1:])
