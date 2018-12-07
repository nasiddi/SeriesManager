
from utils.io_utlis import load_shows


def get_series_name(s):
    return s.series_name


shows = load_shows(read_only=True)

for show in sorted(shows.values(), key=lambda k: k.series_name):
    for season in sorted(show.seasons.values(), key=lambda k: k.s_nr):
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            if not episode.quality:
                print(episode.id())







