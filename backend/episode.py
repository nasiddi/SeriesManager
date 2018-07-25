import os
import re
import warnings
from constants import *


class Episode:
    def __init__(self, location='', e_nr=999, s_nr=0):
        self.location = location
        self.file_name = os.path.basename(location)
        self.format = ''
        self.s_nr = s_nr
        self.anime = False
        if os.path.normpath(location).split(os.path.sep)[1] == 'Anime':
            self.anime = True
        self.double = False
        self.triple = False
        self.e_nr = e_nr
        self.previous = None
        self.next = None
        self.e_name = ''
        self.e_name2 = ''
        if e_nr == 999:
            self.parse_episode_nr()
        self.parse_episode_name_and_extention()

    def parse_episode_name_and_extention(self):
        file_name = self.file_name
        dot = file_name.rfind('.')
        self.format = file_name[dot+1:]
        name = file_name[:dot]
        match = re.findall(re.compile(SERIES_PATTERN), name)
        if not match:
            return
        pattern_index = name.find(match[-1])
        if ' - ' not in name[pattern_index:]:
            return
        name = name[pattern_index:].split(' - ', 1)[1]
        if self.double:
            if '&' in name:
                name = name.split('&')
                self.e_name = name[0]
                self.e_name2 = name[1]
            else:
                self.e_name = name
                self.e_name2 = '++double++'
        else:
            self.e_name = name

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
                self.double = True
            return

        if len(match) == 3:
            triple_pattern = re.compile(single_pattern + '\s&\s' + single_pattern + '\s&\s' + single_pattern)
            if re.findall(triple_pattern, self.file_name):
                self.triple = True












