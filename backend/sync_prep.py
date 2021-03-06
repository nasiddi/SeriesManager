import re
from os import path, sep, walk, environ
from sys import argv

from utils.constants import FILE_DIR, EXTENSIONS, SUBS, ENDED, MAC_OFFSET, OUT_FILE, CONF_FILE
from utils.file import File
from utils.io_utlis import load_shows, parse_args, save_json, load_json


def main(args):
    parse_args(args)
    conf = load_json(environ[CONF_FILE])
    save_json(conf, 'data/sync_prep.json')
    shows = load_shows(read_only=True)
    file_list = []
    subs = []
    for root, dirs, files in walk(FILE_DIR):
        for name in files:
            if '[ignore]' in root or '[ignore]' in name:
                continue
            extension = name.split('.')[-1].lower()
            if extension in EXTENSIONS:
                if 'sample' in name.lower():
                    continue
                file_list.append(File(old_location=path.join(root, name)))
            if extension in SUBS:
                subs.append({'text': name, 'value': path.join(root, name)})

    series_names_words = []
    series_names = []
    series_n = sorted(list(shows.keys()))
    for n in series_n:
        if shows[n].status == ENDED:
            continue
        n1 = clean_up(n)
        series_names_words.append(n1)
        series_names.append(n)
        n2 = n.replace('\'', '')
        n2 = n2.replace('.', '')
        n2 = n2.replace(',', '')
        n2 = clean_up(n2)

        if not set(n1) == set(n2):
            series_names.append(n)
            series_names_words.append(n2)
    print(series_names)

    if not conf['all']:
        remove_folders_with_multiple_files(file_list)

    i = 0
    for file in file_list:
        file.file_id = i
        i += 1

    regex = [
        {
            "e_end": 6,
            "e_start": 4,
            "regex": "s[0-9]{2}e[0-9]{2}",
            "s_end": 3,
            "s_start": 1,
        },
        {
            "e_end": 5,
            "e_start": 3,
            "regex": "[0-9]{2}x[0-9]{2}",
            "s_end": 2,
            "s_start": 0,
        },
    ]
    for file in file_list:
        location = file.old_location.lower()
        for reg in regex:

            pattern = re.compile(reg['regex'])
            match = re.findall(pattern, location)
            if match:
                try:
                    file.s_nr = int(match[0][reg['s_start']:reg['s_end']])
                    file.e_nr = int(match[0][reg['e_start']:reg['e_end']])
                    break
                except IndexError:
                    continue
        for name in series_names_words:
            if all(word in location for word in name):
                index = series_names_words.index(name)
                file.series_name = series_names[index]

    n_series = {}

    for n in list(shows.keys()):
        n_series[n] = {'tvdb_id': shows[n].tvdb_id, 'name_needed': shows[n].name_needed}

    n_series['Series Name'] = 0

    json = {'shows': n_series, 'files': [], 'subs': subs}
    for file in file_list:
        json['files'].append(file.__str__())

    save_json(json, environ[OUT_FILE])
    pass


def remove_folders_with_multiple_files(file_list):
    locations = []
    multi_title = []
    delete = []
    for file in file_list:
        loc = file.old_location.split(sep)[2 + MAC_OFFSET]
        if loc in locations:
            if loc not in multi_title:
                multi_title.append(loc)
        else:
            locations.append(loc)
    for file in file_list:
        loc = file.old_location.split(sep)[2 + MAC_OFFSET]
        if loc in multi_title:
            delete.append(file)
    for file in delete:
        file_list.remove(file)


def clean_up(n):
    n = n.lower().split(' ')
    while 'the' in n:
        n.remove('the')
    while '-' in n:
        n.remove('-')
    while '&' in n:
        n.remove('&')
    return n


if __name__ == '__main__':
    main(argv[1:])
