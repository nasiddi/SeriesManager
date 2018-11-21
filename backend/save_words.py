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
    io_utlis.save_json(data, 'data/save_words.json')

    SHOWS = io_utlis.load_shows()
    dictionary = io_utlis.load_json('data/dictionary.json')
    print(len(dictionary))
    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return

    for file in data:
        changes = []
        for w in file['words']:
            if w['add'] and w['word'] not in dictionary:
                dictionary.append(w['word'])
            if w['changed']:
                changes.append([w['key'], w['word']])

        if changes:
            old = file['file']
            for c in changes:
                file['file'] = file['file'].replace(c[0], c[1])
            print(file['location'])
            file['location'] = file['location'].replace(old, file['file'])
            print(file['location'])
    print(len(dictionary))





if __name__ == '__main__':
    main(sys.argv[1:])