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
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["CONF_FILE"])
    # io_utlis.save_json(data, 'data/save_words.json')

    SHOWS = io_utlis.load_shows()
    dictionary = io_utlis.load_json(DICT_FILE)

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
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
            old = file['file'].rsplit('.', 1)
            words = words = old[0].split(' ')
            for c in changes:
                words[c[0]] = c[1]
            words = list(filter(None, words))
            file['file'] = ' '.join(words)
            new_location = file['location'].replace(old[0], file['file'])
            try:
                shutil.move(file['location'], new_location)
            except Exception as e:
                print('rename', e)

    io_utlis.save_json(dictionary, DICT_FILE)
    io_utlis.save_shows(SHOWS)






if __name__ == '__main__':
    main(sys.argv[1:])