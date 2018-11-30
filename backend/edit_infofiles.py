from constants import *
import io_utlis
import sys



def main(args):

    order = {'double': {'title': 'DoubleTitle', 'order': 5},
             'lower': {'title': 'lowerCase', 'order': 1},
             'upper': {'title': 'UpperCase', 'order': 2},
             'lower_general': {'title': 'lowerGeneral', 'order': 3},
             'part': {'title': 'Part', 'order': 4}}
    io_utlis.parse_args(args)
    exceptions = io_utlis.load_json(EXCEPTIONS_FILE)

    files = [structure(k, v) for k, v in exceptions.items()]
    d = {}
    for f in files:
        k = list(f.keys())[0]
        d[order[k]['order']] = {'items': f[k], 'open': False, 'title': order[k]['title'], 'key': k}

    io_utlis.save_json(d, os.environ[OUT_FILE])


def structure(k, l):
    if type(l) is dict:
        return {k: [item for sublist in [flatten(k, v) for k, v in l.items()] for item in sublist]}
    return {k: flatten('', l)}


def flatten(k, v):
    return [{'origin': k, 'text': item, 'delete': False, 'key': k + item} for item in v]


if __name__ == '__main__':
    main(sys.argv[1:])