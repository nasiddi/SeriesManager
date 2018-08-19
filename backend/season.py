

class Season:
    def __init__(self, s_nr=0, episodes={}, episode_count=0, location=''):

        self.s_nr = s_nr
        self.episodes = episodes
        self.episode_count = episode_count
        self.location = location
        self.previous = None
        self.next = None

    def save(self):
        episodes = {}
        for episode in self.episodes.keys():
            episodes[episode] = self.episodes[episode].save()
        return episodes

