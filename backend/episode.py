import re
import shutil
import warnings
from os import path, sep

from utils.constants import SINGLE, DOUBLE, TRIPLE, MAC_OFFSET, ANIME_PATTERN, SERIES_PATTERN


class Episode:
    def __init__(self, location='',
                 e_nr=999,
                 s_nr=0,
                 series_name='',
                 episode_option=SINGLE,
                 title='',
                 title2='',
                 title3='',
                 duration=0,
                 height=0,
                 width=0,
                 size=0,
                 ratio=0,
                 quality=''):
        self.location = location
        self.series_name = self.location.split(sep)[2 + MAC_OFFSET] if series_name == '' else series_name
        self.file_name = path.basename(location)
        self.extension = ''
        self.s_nr = s_nr
        self.anime = False
        if path.normpath(location).split(path.sep)[1 + MAC_OFFSET] == 'Anime':
            self.anime = True
        self.episode_option = episode_option
        self.e_nr = e_nr
        self.title = title
        self.title2 = title2
        self.title3 = title3
        self.duration = duration
        self.height = height
        self.width = width
        self.size = size
        self.ratio = ratio
        self.quality = quality
        if e_nr == 999:
            self.parse_episode_nr()
        if self.extension == '':
            self.parse_episode_name_and_extension()

    def save(self):
        return {'duration': self.duration,
                'height': self.height,
                'width': self.width,
                'size': self.size,
                'ratio': self.ratio,
                'quality': self.quality}

    def set_file_meta(self, data):
        self.height = data[0]
        self.width = data[1]
        self.size = data[2]
        self.duration = data[3]
        self.ratio = data[4]

    def update_location(self, old_series_name, new_series_name):
        old_loc = self.location.replace(old_series_name, new_series_name, 1)
        self.location = self.location.replace(old_series_name, new_series_name, 2)
        shutil.move(old_loc, self.location)
        self.file_name = path.basename(self.location)

    def parse_episode_name_and_extension(self):
        file_name = self.file_name
        dot = file_name.rfind('.')
        if dot >= 0:
            self.extension = file_name[dot + 1:]
        name = file_name[:dot]
        match = re.findall(re.compile(ANIME_PATTERN if self.anime else SERIES_PATTERN), name)
        if not match:
            return
        pattern_index = name.find(match[-1]) - 1
        if ' - ' not in name[pattern_index:]:
            self.title = ''
            return
        name = name[pattern_index:].split(' - ', 1)[1]
        if self.episode_option == DOUBLE:
            if ' & ' in name:
                name = name.split(' & ')
                self.title = name[0]
                self.title2 = name[1]
            else:
                self.title = name
        else:
            self.title = name

    def get_title(self):
        if not self.title:
            return ''
        if self.episode_option == DOUBLE:
            if self.title2:
                return '&'.join([self.title, self.title2])
        elif self.episode_option == TRIPLE:
            if self.title2 and self.title3:
                return '&'.join([self.title, self.title2, self.title3])
        return self.title

    def parse_episode_nr(self):
        if self.anime:
            single_pattern = ANIME_PATTERN
        else:
            single_pattern = SERIES_PATTERN
        pattern = re.compile(single_pattern)

        match = re.findall(pattern, self.file_name)
        self.e_nr = int(match[0][4:-1]) if match else 999
        if self.e_nr == 999:
            warnings.warn('cannot parse episode nr of\n' + self.location)

        if self.s_nr == 0 and match:
            self.s_nr = int(match[0][:3])
        if len(match) <= 1:
            return

        if len(match) == 2:
            double_pattern = re.compile(single_pattern + '&' + single_pattern)
            if re.findall(double_pattern, self.file_name):
                self.episode_option = DOUBLE
            return

        if len(match) == 3:
            triple_pattern = re.compile(single_pattern + '&' + single_pattern + '&' + single_pattern)
            if re.findall(triple_pattern, self.file_name):
                self.episode_option = TRIPLE

    def __str__(self):
        return ('***' +
                '\nShow: ' + self.location.split(sep)[2 + MAC_OFFSET] + ' SNr: ' + str(self.s_nr)
                + ' ENr: ' + str(self.e_nr) +
                '\nFilename: ' + self.file_name +
                '\nDuration: ' + str(self.duration) + ' Size: ' + str(self.size))

    def id(self):
        return f'{self.series_name} {self.s_nr:02d}x{self.e_nr:0{3 if self.anime else 2}d}'

    def compile_file_name(self, file=None):
        if not file:
            file = self
        pad = 3 if file.anime else 2
        if file.episode_option == 'Single':
            if file.title == '':
                return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d}.{file.extension}'
            return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d} - {file.title}.{file.extension}'
        elif file.episode_option == 'Double':
            if file.title == '' and file.title2 == '':
                return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d}' \
                       f' & {file.s_nr:02d}x{file.e_nr + 1:0{pad}d}.{file.extension}'
            if not file.title == file.title2 and not (file.title == '' or file.title2 == ''):
                return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d}' \
                       f' & {file.s_nr:02d}x{file.e_nr + 1:0{pad}d} - {file.title} & {file.title2}.{file.extension}'
            return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d} & ' \
                   f'{file.s_nr:02d}x{file.e_nr + 1:0{pad}d}' \
                   f' - {file.title if not file.title == "" else file.title2}.{file.extension}'
        else:
            seen = set()
            titles = filter(None, [file.title, file.title2, file.title3])
            title_set = [x for x in titles if not (x in seen or seen.add(x))]
            # one title
            if len(title_set) == 1:
                return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d} & ' \
                       f'{file.s_nr:02d}x{file.e_nr + 1:0{pad}d} & ' \
                       f'{file.s_nr:02d}x{file.e_nr + 2:0{pad}d} - {title_set[0]}.{file.extension}'
            elif len(title_set) == 2:
                return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d} & ' \
                       f'{file.s_nr:02d}x{file.e_nr + 1:0{pad}d} & {file.s_nr:02d}x{file.e_nr + 2:0{pad}d}' \
                       f' - {title_set[0]} & {title_set[1]}.{file.extension}'
            elif len(title_set) == 3:
                return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d} & {file.s_nr:02d}' \
                       f'x{file.e_nr + 1:0{pad}d} & {file.s_nr:02d}x{file.e_nr + 2:0{pad}d}' \
                       f' - {file.title} & {file.title2} & {file.title3}.{file.extension}'
            # no title
            return f'{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d} & {file.s_nr:02d}' \
                   f'x{file.e_nr + 1:0{pad}d} & {file.s_nr:02d}x{file.e_nr + 2:0{pad}d}.{file.extension}'



