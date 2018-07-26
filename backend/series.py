from constants import *
from season import Season

class Series:

    def __init__(self, series_name='', short='', season_count=0, name_needed=False, status=NONE, location=''):
        self.series_name = series_name
        self.short = short
        self. season_count = season_count
        self.name_needed = name_needed
        self.status = status
        self.location = location
        self.seasons = {}
        self.last_ep = None
        self.premiere = ''
        self.final = ''
        self.names = {}
        self.tvdb_id = 0

    def __str__(self):
        return ('Name:\t\t' + self.series_name +
                '\nShort:\t\t' + self.short +
                '\nSeasons:\t' + str(self.season_count) +
                '\nStatus:\t\t' + self.status +
                '\nLocation:\t' + self.location)

    def add_season(self, location='', number=0):
        if number == 0:
            number = int(location[-2:])
        self.seasons[number] = Season(location=location, s_nr=number)






