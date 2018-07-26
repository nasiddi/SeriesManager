from constants import *
import os
from file import File
import re
import io_utlis
import sys


def main(args):
    io_utlis.parse_args(args)
    shows = io_utlis.pickle_load('shows')
    file_list = []
    subs = []
    for root, dirs, files in os.walk(FILE_DIR):
        for name in files:
            extention = name.split('.')[-1].lower()
            if extention in EXTENTIONS:
                if 'sample' in name.lower():
                    continue
                file_list.append(File(location=os.path.join(root, name)))
            if extention in SUBS:
                subs.append({'text': name, 'value': os.path.join(root, name)})

    series_names = []
    series_n = shows.keys()
    for n in series_n:
        n = n.lower().split(' ')
        while 'The' in n:
            n.remove('The')
        while '-' in n:
            n.remove('-')
        series_names.append(n)

    locations = []
    multis = []
    delete = []
    for file in file_list:
        loc = file.location.split('\\')[2]
        if loc in locations:
            if loc not in multis:
                multis.append(loc)
        else:
            locations.append(loc)

    for file in file_list:
        loc = file.location.split('\\')[2]
        if loc in multis:
            delete.append(file)

    for file in delete:
        file_list.remove(file)

    i = 0
    for file in file_list:
        file.file_id = i
        i += 1

    pattern = re.compile('s[0-9]{2}e[0-9]{2}')
    for file in file_list:
        location = file.location.lower()
        match = re.findall(pattern, location)
        if match:
            file.s_nr = int(match[0][1:3])
            file.e_nr = int(match[0][4:])
        if file.s_nr == 1 and file.e_nr == 11:
            pass
        for name in series_names:
            if all(word in location for word in name):
                index = series_names.index(name)
                file.series_name = list(series_n)[index]
                show = shows[file.series_name]

    n_series = {}

    for n in list(shows.keys()):
        n_series[n] = shows[n].tvdb_id

    n_series['Series Name'] = 0

    json = {'shows': n_series, 'files': [], 'subs': subs}
    for file in file_list:
        json['files'].append(file.__str__())

    io_utlis.save_json(json, os.environ['OUTPUT_FILE'])
    pass


if __name__ == '__main__':
    main(sys.argv[1:])


