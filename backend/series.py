from os import sep

from season import Season
from utils.constants import NONE, ANIME_DIR, SINGLE, DOUBLE, TRIPLE


class Series:
    def __init__(self, series_name='',
                 name_needed=False,
                 status=NONE,
                 location='',
                 tvdb_id='',
                 premiere='',
                 final=''):
        self.series_name = series_name
        self.name_needed = name_needed
        self.status = status
        self.location = location
        self.seasons = {}
        self.premiere = premiere
        self.final = final
        self.tvdb_id = tvdb_id if not tvdb_id == 0 else ''
        self.anime = True if ANIME_DIR in self.location else False

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
            'tvdb_id': self.tvdb_id,
            'seasons': self.save_seasons()
        }}

    def save_seasons(self):
        seasons = {}
        for season in self.seasons.keys():
            seasons[season] = self.seasons[season].save()
        return seasons

    def add_season(self, location='', number=0):
        if number == 0:
            number = int(location[-2:])
        season = Season(location=location, s_nr=number)
        season.episodes = {}
        self.seasons[number] = season
        return season

    def get_episode_by_sxe(self, s_nr, e_nr):
        try:
            return self.seasons[s_nr].episodes[e_nr]
        except Exception:
            try:
                e = self.seasons[s_nr].episodes[e_nr - 1]
                if not e.episode_option == SINGLE:
                    return e
            except Exception:
                try:
                    e = self.seasons[s_nr].episodes[e_nr - 2]
                    if e.episode_option == TRIPLE:
                        return e
                except Exception:
                    return None
            return None

    def add_episode(self, episode):
        new_season = False
        if episode.s_nr not in self.seasons:
            self.add_season(location=sep.join(episode.location.split(sep)[:-1]), number=episode.s_nr)
            new_season = True
        season = self.seasons[episode.s_nr]
        if episode.e_nr in season.episode_numbers:
            if not episode.e_nr == 999:
                episode.e_nr = 777
        while episode.e_nr in season.episodes:
            episode.e_nr += 1
        season.episodes[episode.e_nr] = episode
        if episode.e_nr < 777:
            season.episode_numbers.append(episode.e_nr)
            if episode.episode_option == DOUBLE:
                season.episode_numbers.append(episode.e_nr + 1)
            if episode.episode_option == TRIPLE:
                season.episode_numbers.append(episode.e_nr + 2)
        sorted(season.episode_numbers)
        return new_season

    def get_next(self, episode):
        e_keys = sorted(self.seasons[episode.s_nr].episodes.keys())
        index = e_keys.index(episode.e_nr)
        if len(e_keys) > index + 1:
            return self.seasons[episode.s_nr].episodes[e_keys[index + 1]]
        s_keys = sorted(self.seasons.keys())
        index = s_keys.index(episode.s_nr)
        if len(s_keys) == index + 1:
            return None
        season = self.seasons[s_keys[index + 1]]
        e = min(season.episodes.keys())
        return season.episodes[e]

    def get_previous(self, episode):
        e_keys = sorted(self.seasons[episode.s_nr].episodes.keys())
        index = e_keys.index(episode.e_nr)
        if index > 0:
            return self.seasons[episode.s_nr].episodes[e_keys[index - 1]]
        s_keys = sorted(self.seasons.keys())
        index = s_keys.index(episode.s_nr)
        if index == 0:
            return None
        season = self.seasons[s_keys[index - 1]]
        e = max(season.episodes.keys())
        return season.episodes[e]

    def get_last_episode(self):
        last_season = self.seasons[max(self.seasons.keys())]
        return last_season.episodes[max(last_season.episodes.keys())]

    def update_metadata(self):
        for season in self.seasons.values():
            for e in season.episodes.values():
                e.update_file_meta()
