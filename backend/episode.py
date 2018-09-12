import os
import re
import warnings
from constants import *
import shutil


class Episode:
    def __init__(self, location='',
                 e_nr=999,
                 s_nr=0,
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
        self.file_name = os.path.basename(location)
        self.extention = ''
        self.s_nr = s_nr
        self.anime = False
        if os.path.normpath(location).split(os.path.sep)[1 + MAC_OFFSET] == 'Anime':
            self.anime = True
        self.episode_option = episode_option
        self.e_nr = e_nr
        self.previous = None
        self.next = None
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
        if self.extention == '':
            self.parse_episode_name_and_extention()

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
        self.aspect = data[4]

    def update_location(self, old_series_name, new_series_name):
        old_loc = self.location.replace(old_series_name, new_series_name, 1)
        self.location = self.location.replace(old_series_name, new_series_name, 2)
        shutil.move(old_loc, self.location)
        self.file_name = os.path.basename(self.location)

    def parse_episode_name_and_extention(self):
        file_name = self.file_name
        dot = file_name.rfind('.')
        if dot >= 0:
            self.extention = file_name[dot+1:]
        name = file_name[:dot]
        match = re.findall(re.compile(SERIES_PATTERN), name)
        if not match:
            return
        pattern_index = name.find(match[-1])
        if ' - ' not in name[pattern_index:]:
            return
        name = name[pattern_index:].split(' - ', 1)[1]
        if self.episode_option == DOUBLE:
            if '&' in name:
                name = name.split('&')
                self.title = name[0]
                self.title2 = name[1]
            else:
                self.title = name
                self.title2 = name
        else:
            self.title = name

    def parse_episode_nr(self):
        if self.anime:
            single_pattern = ANIME_PATTERN
        else:
            single_pattern = SERIES_PATTERN
        pattern = re.compile(single_pattern)

        match = re.findall(pattern, self.file_name)
        self.e_nr = int(match[0][3:]) if match else 999

        if self.e_nr == 999:
            warnings.warn('cannot parse episode nr of\n' + self.location)

        if len(match) == 1:
            return

        if len(match) == 2:
            double_pattern = re.compile(single_pattern + '\s&\s' + single_pattern)
            if re.findall(double_pattern, self.file_name):
                self.episode_option = DOUBLE
            return

        if len(match) == 3:
            triple_pattern = re.compile(single_pattern + '\s&\s' + single_pattern + '\s&\s' + single_pattern)
            if re.findall(triple_pattern, self.file_name):
                self.episode_option = TRIPLE

    def __str__(self):
        return ('***' +
                '\nShow: ' + self.location.split(SEPERATOR)[2 + MAC_OFFSET] + ' SNr: ' + str(self.s_nr) + ' ENr: ' + str(self.e_nr) +
                '\nFilename: ' + self.file_name +
                '\nDuration: ' + str(self.duration) + ' Size: ' + str(self.size))











