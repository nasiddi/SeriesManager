from utils import io_utlis
import random

stats = io_utlis.load_json('data/stats_file.json')

shows = stats['shows']
random.shuffle(shows)


def find(string, ch):
    return [i for i, ltr in enumerate(string) if ltr == ch]


while shows:
    show = shows.pop()
    s = f"Episodes: {show['episodes']}\nSeasons: {show['seasons']}\n" \
        f"Status: {list(show['status'].keys())[0]}\n" \
        f"Premiere: {show['premiere']} Final: {show['final']}\n" \
        f"Extension: {show['extension']}\n" \
        f"Quality: {show['quality']}\n" \
        f"Duration: {show['avg_duration']} min avg / {show['duration']} h total"

    print(s)
    h = 'h'
    series_name = show['series_name']
    indexes = list(range(0, len(series_name)))
    spaces = find(series_name, ' ')
    for space in spaces:
        indexes.remove(space)
    random.shuffle(indexes)
    hint = ''.ljust(200)
    while h == 'h' and indexes:
        h = input()
        if h == 'h':
            index = indexes.pop(0)
            hint = list(hint)
            hint[index] = series_name[index]
            hint = ''.join(hint)
            print(hint)

    print(series_name)
    print('\n*****************\n')
