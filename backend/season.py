from os import listdir, path

from episode import Episode


class Season:
    def __init__(self, s_nr=0, location=''):

        self.s_nr = s_nr
        self.episodes = {}
        self.episode_count = 0
        self.episode_numbers = []
        self.location = location

    def save(self):
        episodes = {}
        for episode in self.episodes.keys():
            episodes[episode] = self.episodes[episode].save()
        return episodes

    def update_episodes(self, reload_metadata=True):
        self.episodes = {}
        files = listdir(self.location)
        for file in files:
            episode = Episode(location=path.join(self.location, file), s_nr=self.s_nr)
            if reload_metadata:
                episode.update_file_meta()
            if episode.e_nr in self.episode_numbers:
                if not episode.e_nr == 999:
                    episode.e_nr = 777
            while episode.e_nr in self.episodes:
                episode.e_nr += 1
            self.episodes[episode.e_nr] = episode
            if episode.e_nr < 777:
                self.episode_numbers.append(episode.e_nr)
        sorted(self.episode_numbers)
