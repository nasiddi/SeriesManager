from mongoengine import *
import pickle
from series import Series
from episode import Episode
from datetime import datetime
from dateutil.relativedelta import relativedelta

db = connect('atlantis', host='localhost', port=27017)


def fill_db_from_pickle():
    db.drop_database('atlantis')

    SHOWS = pickle_load('shows.pkl')
    s: Series
    for s in sorted(list(SHOWS.values()), key=lambda k: k.series_name.lower()):
        Show(
            show_id=s.series_name,
            name_needed=s.name_needed,
            status=s.status,
            location=s.location,
            premiere=datetime.strptime(s.premiere, '%Y-%m-%d') if s.premiere else None,
            final=datetime.strptime(s.final, '%Y-%m-%d') if s.final else None
        ).save()
        for sea in sorted(list(s.seasons.values()), key=lambda k: k.s_nr):
            season = S(
                s_nr=sea.s_nr,
                season_id=f'{s.series_name} {sea.s_nr:02d}',
                show_id=s.series_name,
                location=sea.location,
            ).save()
            e: Episode
            for e in sorted(list(sea.episodes.values()), key=lambda k: k.e_nr):
                E(
                    episode_id=e.id(),
                    location=e.location,
                    show_id=s.series_name,
                    file_name=e.file_name,
                    extension=e.extension,
                    season_id=season.season_id,
                    anime=e.anime,
                    episode_option=e.episode_option,
                    e_nr=e.e_nr,
                    duration=e.duration,
                    height=e.height,
                    width=e.width,
                    size=e.size,
                    ratio=e.ratio,
                    quality=e.quality,
                    title=e.title
                ).save()


    s = Show.objects(show_id='Star Trek')[0]
    s.premiere = datetime.strptime('1966-09-08', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='The Magicians')[0]
    s.premiere = datetime.strptime('2015-12-16', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='The Musketeers')[0]
    s.premiere = datetime.strptime('2014-01-19', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='Star Trek - Deep Space Nine')[0]
    s.final = datetime.strptime('1999-06-02', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='Star Trek - Voyager')[0]
    s.final = datetime.strptime('2001-05-23', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='Star Trek - Enterprise')[0]
    s.final = datetime.strptime('2005-05-13', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='Firefly')[0]
    s.final = datetime.strptime('2002-12-20', '%Y-%m-%d')
    s.save()

    s = Show.objects(show_id='Naruto')[0]
    s.final = datetime.strptime('2007-02-08', '%Y-%m-%d')
    s.save()

    for show in Show.objects:
        show.density = get_density(show)
        show.save()


def pickle_load(file):
    with open(file, "rb") as f:
        return pickle.load(f)


class E(Document):
    location = StringField()
    show_id = StringField()
    file_name = StringField()
    extension = StringField(max_length=10)
    season_id = StringField()
    anime = BooleanField()
    episode_option = StringField()
    e_nr = IntField()
    episode_id = StringField()
    duration = FloatField()
    height = IntField()
    width = IntField()
    size = FloatField()
    ratio = FloatField()
    quality = StringField()
    title = StringField()

    def __str__(self):
        return self.episode_id


class S(Document):
    s_nr = IntField(min_value=0)
    season_id = StringField()
    location = StringField()
    show_id = StringField()

    def __str__(self):
        return self.season_id


class Show(Document):
    show_id = StringField(required=True)
    name_needed = BooleanField()
    status = StringField(max_length=7)
    location = StringField()
    premiere = DateField()
    final = DateField()
    density = FloatField()

    def __str__(self):
        return self.show_id


def get_diff_in_years(premiere, final):
    if not premiere:
        return '     '
    if not final:
        final = datetime.today()
    diff = relativedelta(final, premiere)
    total = diff.years
    total += diff.days / 365
    total += diff.months / 12
    return "{0: >5}".format("{:4.2f}".format(total))


def get_density(show):
    diff = get_diff_in_years(show.premiere, show.final)
    e_count = E.objects(show_id=show.show_id).count()
    return e_count / float(diff) if float(diff) > 1 else e_count


# fill_db_from_pickle()


for s in ['Airing', 'Hiatus', 'Ended']:
    print(s, Show.objects(status__exact=s).count())

print(E.objects.sum('duration') / 60 / 24)

episodes = E.objects(e_nr=2, title__contains='Pilot')

for e in episodes:
    shows = Show.objects(show_id=e.show_id)
    print(shows[0].status, e, e.title)

print()
for show in Show.objects.order_by('-density'):
    diff = get_diff_in_years(show.premiere, show.final)
    density = "{0: >5}".format("{:4.2f}".format(show.density))
    print(show.premiere if show.premiere else '          ', show.final if show.final else '          ',
          diff, density, show)
print()
print(len(Show.objects))
print()
dates = []
for show in Show.objects.order_by('premiere'):
    names = []
    if show.premiere not in dates and show.final is not None:
        names.append([show.show_id, 'premiere'])
        matches = Show.objects(premiere=show.premiere)
        if matches:
            dates.append(show.premiere)
            for match in matches:
                if match.show_id == show.show_id:
                    continue
                names.append([match.show_id, 'premiere'])
        matches = Show.objects(final=show.premiere)
        if matches:
            dates.append(show.premiere)
            for match in matches:
                if match.show_id == show.show_id:
                    continue
                names.append([match.show_id, 'final'])
        if len(names) > 1:
            print(show.premiere, names)
    names = []
    if show.final not in dates and show.final is not None:
        matches = Show.objects(final=show.final)
        names.append([show.show_id, 'final'])
        if matches:
            dates.append(show.final)
            for match in matches:
                if match.show_id == show.show_id:
                    continue
                names.append([match.show_id, 'final'])
        if len(names) > 1:
            print(show.final, names)

