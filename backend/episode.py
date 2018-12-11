import re
from shutil import move
from os import path, sep

from utils.io_utlis import find_video_metadata
from utils.constants import SINGLE, DOUBLE, TRIPLE, MAC_OFFSET, ANIME_PATTERN, SERIES_PATTERN, ANIME_DIR, ASPECT_RATIOS, \
    QUALITY


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
        self.series_name = series_name
        self.file_name = ''
        self.extension = ''
        self.s_nr = s_nr
        self.anime = False
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

        self._parse()

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
        move(old_loc, self.location)
        self.file_name = path.basename(self.location)
        self.series_name = new_series_name

    def _parse(self):
        self.file_name = path.basename(self.location)
        series_name = self.location.split(sep)[2 + MAC_OFFSET: 3 + MAC_OFFSET]
        if series_name:
            self.series_name = series_name[0]

        if ANIME_DIR in self.location:
            self.anime = True

        file_name = self.file_name
        file_name = file_name.rsplit('.', 1)
        if len(file_name) > 1:
            self.extension = file_name[1]
        file_name = file_name[0]

        single_pattern = ANIME_PATTERN if self.anime else SERIES_PATTERN
        match = re.findall(re.compile(single_pattern), self.file_name)
        if not match:
            return
        [self.s_nr, self.e_nr] = [int(x.replace('.', '')) for x in match[0].split('x')]
        if len(match) > 1:
            triple_pattern = re.compile(single_pattern + '&' + single_pattern + '&' + single_pattern)
            if re.findall(triple_pattern, self.file_name):
                self.episode_option = TRIPLE
            else:
                double_pattern = re.compile(single_pattern + '&' + single_pattern)
                if re.findall(double_pattern, self.file_name):
                    self.episode_option = DOUBLE
        title = file_name.split(match[-1], 1)
        if len(title) == 1:
            self.title = ''
            return
        title = title[1][2:]
        if self.episode_option == SINGLE:
            self.title = title
            return
        titles = title.split(' & ')
        if len(titles) > 2 and self.episode_option == TRIPLE:
            self.title3 = titles[2]
        if len(titles) == 1:
            self.title = title
            return
        self.title = titles[0]
        self.title2 = titles[1]

    def get_title(self):
        if not self.title:
            return ''
        if self.episode_option == DOUBLE:
            if self.title2:
                return ' & '.join([self.title, self.title2])
        elif self.episode_option == TRIPLE:
            if self.title2 and self.title3:
                return ' & '.join([self.title, self.title2, self.title3])
        return self.title

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
        option = file.episode_option
        seen = set()
        titles = filter(None, [file.title, file.title2 if not option == SINGLE else '',
                               file.title3 if option == TRIPLE else ''])
        title_set = [x for x in titles if not (x in seen or seen.add(x))]

        return f"{file.series_name} {file.s_nr:02d}x{file.e_nr:0{pad}d}"\
               + (f" & {file.s_nr:02d}x{file.e_nr + 1:0{pad}d}" if not option == SINGLE else '')\
               + (f" & {file.s_nr:02d}x{file.e_nr + 2:0{pad}d}" if option == TRIPLE else '')\
               + (f" - {title_set.pop(0)}" if title_set else '')\
               + (f" & {title_set.pop(0)}" if title_set else '')\
               + (f" & {title_set.pop(0)}" if title_set else '')\
               + f".{file.extension}"

    def update_file_meta(self):
        data = find_video_metadata(self.location)
        if data:
            self.set_file_meta(data)

        if self.height == 0 or self.width == 0:
            ratio = ''
        else:
            ratio = int(1000.0 * self.width / self.height) / 1000.0
            ratio = min(ASPECT_RATIOS, key=lambda x: abs(x - ratio))
        self.ratio = ratio
        if self.height == 0:
            self.quality = ''
        else:
            self.quality = QUALITY[min(QUALITY, key=lambda x: abs(x - self.height))]

    def set_location(self, location):
        self.location = location
        self._parse()


