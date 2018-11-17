import io_utlis
import sys
from constants import *
from file import File
import re

SHOWS = None


def main(args):
    global SHOWS
    io_utlis.parse_args(args)
    data = io_utlis.load_json(os.environ["DATA_FILE"])
    io_utlis.save_json(data, 'data/batch_match.json')
    SHOWS = io_utlis.load_shows()

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, os.environ['OUTPUT_FILE'])
        print('shows locked')
        return
    file_list = []
    for u in data['units']:
        if not u['select']:
            continue
        location = os.path.join(FILE_DIR, u['text'])
        if os.path.isfile(location):
            file = prepFile(location, '')
            if file:
                file_list.append(file)
        else:
            for root, dirs, files in os.walk(location):
                for name in files:
                    file = prepFile(name, root)
                    if file:
                        file_list.append(file)


    for reg in data['regex']:
        if not reg['regex']:
            continue
        pattern = re.compile(reg['regex'])
        for file in file_list:
            match = re.findall(pattern, file.location)
            if match:
                try:
                    file.s_nr = int(match[0][reg['s_start']:reg['s_end']])
                    file.e_nr = int(match[0][reg['e_start']:reg['e_end']])
                except IndexError:
                    continue
    output = {'files': []}
    for f in file_list:
        output['files'].append({
            'location': f.location.split(SEPERATOR, 2 + MAC_OFFSET)[2 + MAC_OFFSET],
            'title': '',
            'title2': '',
            'title3': '',
            's_nr': f.s_nr,
            'e_nr': f.e_nr,
            'episode_option': 'Single',
            'sub': f.subs
        })

    output.update({SERIES_NAME: '',
                   TVDB_ID: '',
                   PREMIERE: '',
                   FINAL: '',
                   STATUS: '',
                   'anime': False,
                   NAME_NEEDED: True,
                   })

    io_utlis.save_json(output, os.environ['OUTPUT_FILE'])






    io_utlis.save_shows(SHOWS)


def prepFile(name, root):
    extention = name.split('.')[-1].lower()
    if extention in EXTENTIONS:
        if 'sample' in name.lower():
            return None
        return File(location=os.path.join(root, name), subs=False)
    if extention in SUBS:
        return File(location=os.path.join(root, name), subs=True)




if __name__ == '__main__':
    main(sys.argv[1:])

