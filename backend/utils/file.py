from os import sep

from utils.constants import NONE, SERIES_NAME, FILE_DIR, MAC_OFFSET, AIRING, HIATUS, ENDED


class File:
    def __init__(self,
                 sync=False,
                 old_location='',
                 s_nr='',
                 e_nr='',
                 s_nr_old='',
                 e_nr_old='',
                 series_name='',
                 title='',
                 title2='',
                 title3='',
                 episode_option='Single',
                 override=False,
                 subs=None,
                 type_option='Series',
                 status=NONE,
                 new_series=False,
                 location='',
                 tvdb_id=0,
                 name_needed=True,
                 anime=False,
                 delete=False,
                 ):
        self.old_location = old_location
        self.sync = sync
        self.s_nr = s_nr
        self.e_nr = e_nr
        self.s_nr_old = s_nr_old
        self.e_nr_old = e_nr_old
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
        self.location = location
        self.extension = old_location.split('.')[-1]
        self.status = status
        self.anime = False
        self.new_series = new_series
        self.tvdb_id = tvdb_id
        self.name_needed = name_needed
        self.anime = anime
        self.delete = delete
        self.report = {'info': [], 'error': [], 'success': []}

    def __str__(self):
        return {'location': self.old_location.replace(FILE_DIR, ''),
                SERIES_NAME: self.series_name,
                's_nr': self.s_nr,
                'e_nr': self.e_nr,
                'title': self.title,
                'title2': self.title,
                'title3': self.title,
                'override': False,
                'show_subs': False,
                'new_series': False,
                'sync': False,
                'delete': False,
                't_o': {'s': 'Series', 'o': ['Series', 'HD', 'SD', '[ignore]']},
                'e_o': {'s': 'Single', 'o': ['Single', 'Double', 'Triple']},
                'anime_o': {'s': 'Anime: No', 'o': ['Anime: No', 'Anime: Yes']},
                'name_o': {'s': 'Name required', 'o': ['Name required', 'Name optional']},
                'tvdb_id': '',
                'status_o': {'s': AIRING, 'o': [AIRING, HIATUS, ENDED]},
                'subs': []}

    def get_report(self):
        return dict(file_name=self.location.rsplit(sep, 1)[1] if self.location else
                    self.old_location.split(sep, 2 + MAC_OFFSET)[-1],
                    info=self.report['info'],
                    error=self.report['error'],
                    success=self.report['success'])
