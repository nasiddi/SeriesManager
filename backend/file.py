from constants import *

class File:
    def __init__(self,
                 location='',
                 s_nr='',
                 e_nr='',
                 series_name='Series Name',
                 title='',
                 title2='',
                 title3='',
                 episode_option='Single',
                 override=False,
                 subs=None,
                 type_option='Series'
                 ):
        self.location = location
        self.s_nr = s_nr
        self.e_nr = e_nr
        self.series_name = series_name
        self.title = title
        self.title2 = title2
        self.title3 = title3
        self.episode_option = episode_option
        self.override = override
        self.subs = subs
        self.type_option = type_option
        self.file_id = 0
        self.new_location = ''
        self.extention = '.' + location.split('.')[-1]

    def __str__(self):
        return {'fileID': self.file_id,
                'location': self.location.replace(FILE_DIR, ''),
                'series_name': self.series_name,
                's_nr': self.s_nr,
                'e_nr': self.e_nr,
                'title': self.title,
                'title2': self.title,
                'title3': self.title,
                'override': False,
                'show_subs': False,
                'manual': False,
                'sync': True,
                'type_option': {'selected': 'Series', 'options': ['Series', 'HD', 'SD']},
                'episode_option': {'selected': 'Single', 'options': ['Single', 'Double', 'Triple']},
                'subs': []}


