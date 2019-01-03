from utils import io_utlis
import random

shows = list(io_utlis.load_shows(read_only=True).values())
abc = 'abcdefghijklmnopqrstuvwxyz&\'-.0123456789'
# names = []
# for show in shows:
#     series_name = show.series_name.lower()
#     names.extend(list(series_name))
# print(sorted((list(set(names)))))


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


while True:
    print('\n*****************\n')
    show = random.choice(shows)
    solution = show.series_name
    series_name = solution.lower()
    puzzle = ['_']*len(series_name)
    tried = [' ']*len(abc)
    tried = ''.join(tried)
    spaces = find(series_name, ' ')
    for space in spaces:
        puzzle[space] = ' '
    puzzle = ''.join(puzzle)
    print(puzzle)
    failes = 0
    while '_' in puzzle and failes <= 10:
        entry = input(str(failes) + ':').lower()
        for char in entry:
            tried = list(tried)
            index = abc.index(char)
            tried[index] = char
            tried = ''.join(tried)
            if char in series_name:
                indexes = find(series_name, char)
                puzzle = list(puzzle)
                for i in indexes:
                    puzzle[i] = solution[i]
                puzzle = ''.join(puzzle)
            else:
                failes += 1
        print(puzzle, '|', tried)
    if not puzzle == solution:
        print(solution)




