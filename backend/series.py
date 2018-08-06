from constants import *
from season import Season

class Series:

    def __init__(self, series_name='',
                 season_count=0,
                 name_needed=False,
                 status=NONE,
                 location='',
                 tvdb_id='',
                 anime='',
                 premiere='',
                 final=''):
        self.series_name = series_name
        self.name_needed = name_needed
        self.status = status
        self.location = location
        self.seasons = {}
        self.last_ep = None
        self.premiere = premiere
        self.final = final
        self.names = {}
        self.tvdb_id = tvdb_id if not tvdb_id == 0 else ''
        self.anime = self.is_anime(location) if anime is '' else anime

    def is_anime(self, location):
        return 'Anime' in location

    def __str__(self):
        return ('Name:\t\t' + self.series_name +
                '\nSeasons:\t' + str(len(self.seasons.keys())) +
                '\nStatus:\t\t' + self.status +
                '\nPremiere:\t\t' + self.premiere +
                '\nFinal:\t\t' + self.final +
                '\nTVDB ID:\t\t' + str(self.tvdb_id) +
                '\nLocation:\t' + self.location)

    def save(self):
        return {self.series_name: {
            'name_needed': self.name_needed,
            'status': self.status,
            'premiere': self.premiere,
            'final': self.final,
            'tvdb_id': self.tvdb_id
        }}

    def add_season(self, location='', number=0):
        if number == 0:
            number = int(location[-2:])
        self.seasons[number] = Season(location=location, s_nr=number)

    def get_episode_by_sxe(self, s_nr, e_nr):
        try:
            return self.seasons[s_nr].episodes[e_nr]
        except Exception:
            return None

    def add_episode(self, episode):
        new_season = False
        if episode.s_nr not in self.seasons:
            self.add_season(location=episode.location.split('\\')[-1:], number=episode.s_nr)
            new_season = True
        self.seasons[episode.s_nr].episodes.update({episode.e_nr: episode})
        return new_season




