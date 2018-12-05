from os import listdir, path

from episode import Episode


class Season:
    def __init__(self, s_nr=0, episodes=None, episode_count=0, location=''):

        self.s_nr = s_nr
        self.episodes = episodes
        self.episode_count = episode_count
        self.location = location

    def save(self):
        episodes = {}
        for episode in self.episodes.keys():
            episodes[episode] = self.episodes[episode].save()
        return episodes

    def update_episodes(self):
        self.episodes = {}
        files = listdir(self.location)
        for file in files:
            episode = Episode(location=path.join(self.location, file), s_nr=self.s_nr)
            if episode.anime:
                print(episode)
            if episode.e_nr in self.episodes:
                if not episode.e_nr == 999:
                    episode.e_nr = 777
            while episode.e_nr in self.episodes:
                episode.e_nr += 1
            self.episodes[episode.e_nr] = episode
