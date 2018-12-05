from shutil import move
from os import environ
from sys import argv

from episode import Episode
from io_utlis import load_shows, parse_args, save_json, save_shows, load_json
from constants import DICT_FILE, OUT_FILE, CONF_FILE

SHOWS = None


def main(args):
    global SHOWS
    parse_args(args)
    data = load_json(environ[CONF_FILE])
    save_json(data, 'data/save_words.json')
    SHOWS = load_shows()
    dictionary = load_json(DICT_FILE)

    if SHOWS is None:
        save_json({'shows_locked': True}, environ[OUT_FILE])
        print('shows locked')
        return

    for file in data['words']:
        changes = []
        for w in file['words']:
            if w['add'] and w['word'] not in dictionary:
                dictionary.append(w['word'])
            if w['changed']:
                changes.append([w['index'], w['word']])

        if changes:
            e = Episode(location=file['location'])
            old = file['file'].rsplit('.', 1)
            words = old[0].split(' ')
            for c in changes:
                words[c[0]] = c[1]
            words = list(filter(None, words))
            file['file'] = ' '.join(words)
            new_location = file['location'].replace(old[0], file['file'])
            try:
                move(file['location'], new_location)
                SHOWS[e.series_name].seasons[e.s_nr].update_episodes()
            except Exception as e:
                print('rename', e)

    save_json(dictionary, DICT_FILE)
    save_json({'done': True}, environ[OUT_FILE])
    save_shows(SHOWS)


if __name__ == '__main__':
    main(argv[1:])
