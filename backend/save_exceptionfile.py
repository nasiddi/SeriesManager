from constants import *
SHOWS = None


def main(args):
    global SHOWS
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["CONF_FILE"])
    io_utlis.save_json(data, 'data/save_infofiles.json')

    exceptions = io_utlis.load_json(EXCEPTIONS_FILE)
    data = list(data.values())
    for d in data:
        for i in d['items']:
            if i['delete']:
                if type(exceptions[d['key']]) is dict:
                    exceptions[d['key']][i['origin']].remove(i['text'])
                    if not exceptions[d['key']][i['origin']]:
                        del exceptions[d['key']][i['origin']]
                else:
                    exceptions[d['key']].remove(i['text'])
    io_utlis.save_json({'done': True}, os.environ[OUT_FILE])
    io_utlis.save_json(exceptions, EXCEPTIONS_FILE)


if __name__ == '__main__':
    main(sys.argv[1:])
