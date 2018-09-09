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
                 type_option='Series',
                 status=NONE,
                 new_series=False,
                 new_location='',
                 tvdb_id=0,
                 name_needed=True,
                 anime=False,
                 ):
        self.location = location
        self.s_nr = s_nr
        self.e_nr = e_nr
        self.e_nr2 = int(e_nr) + 1 if type(e_nr) == int else ''
        self.e_nr3 = int(e_nr) + 2 if type(e_nr) == int else ''
        self.series_name = series_name
        self.title = title
        self.title2 = title2
        self.title3 = title3
        self.episode_option = episode_option
        self.override = override
        self.subs = subs
        self.type_option = type_option
        self.new_location = new_location
        self.extention = location.split('.')[-1]
        self.status = status
        self.anime = False
        self.new_series = new_series
        self.tvdb_id = tvdb_id
        self.name_needed = name_needed
        self.anime = anime
        self.report = {'info': [], 'error': [], 'success': []}

    def __str__(self):
        return {'location': self.location.replace(FILE_DIR, ''),
                'series_name': self.series_name,
                's_nr': self.s_nr,
                'e_nr': self.e_nr,
                'title': self.title,
                'title2': self.title,
                'title3': self.title,
                'override': False,
                'show_subs': False,
                'new_series': False,
                'sync': False,
                't_o': {'s': 'Series', 'o': ['Series', 'HD', 'SD']},
                'e_o': {'s': 'Single', 'o': ['Single', 'Double', 'Triple']},
                'anime_o': {'s': 'Anime: No', 'o': ['Anime: No', 'Anime: Yes']},
                'name_o': {'s': 'Name required', 'o': ['Name required', 'Name optional']},
                'tvdb_id': '',
                'status_o': {'s': AIRING, 'o': [AIRING, HIATUS, ENDED]},
                'subs': []}

    def get_report(self):
        return {
            'file_name': self.new_location.rsplit(SEPERATOR, 1)[1],
            'info': self.report['info'],
            'error': self.report['error'],
            'success': self.report['success']}


