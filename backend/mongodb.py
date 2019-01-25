from mongoengine import *
import pickle
from series import Series
from episode import Episode
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import matplotlib.pyplot as plt
import pandas as pd

db = connect('atlantis', host='localhost', port=27017)


def fill_db_from_pickle():
    db.drop_database('atlantis')

    SHOWS = pickle_load('assets/shows.pkl')
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
                    #duration=e.duration,
                    #height=e.height,
                    #width=e.width,
                    #size=e.size,
                    #ratio=e.ratio,
                    #quality=e.quality,
                    title=e.title,
                    air_date=datetime.strptime(e.air_date, '%Y-%m-%d') if e.air_date else None

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
    air_date = DateField()

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


for status in ['Airing', 'Hiatus', 'Ended']:
    print(status, Show.objects(status__exact=status).count())

print(E.objects.sum('duration') / 60 / 24)

episodes = E.objects(e_nr=2, title__contains='Pilot')

for e in episodes:
    shows = Show.objects(show_id=e.show_id)
    print(shows[0].status, e, e.title)

print()
for show in Show.objects.order_by('premiere'):
    diff = get_diff_in_years(show.premiere, show.final)
    density = "{0: >5}".format("{:4.2f}".format(show.density))
    print(show.premiere if show.premiere else '          ', show.final if show.final else '          ',
          diff, density, show)
print()
print(len(Show.objects))
print()


def find_date_matches(show_date, show_id, date_type, dates, matched):
    matches = Show.objects((Q(premiere=show_date) or Q(final=show_date)))
    if len(matches) > 1:
        dates.append(show_date)
        if show_date not in matched:
            matched[show_date] = {'premiere': [], 'final': []}
        matched[show_date][date_type].append(show_id)
        for match in matches:
            if match.premiere == show_date and match.show_id not in matched[show_date]['premiere']:
                matched[show_date]['premiere'].append(match.show_id)
            elif match.final == show_date and match.show_id not in matched[show_date]['final']:
                matched[show_date]['final'].append(match.show_id)


def find_all_matching_dates():
    matched = {}
    dates = []
    for show in Show.objects.order_by('premiere'):
        if show.premiere is not None:
            find_date_matches(show.premiere.strftime('%Y-%m-%d'), show.show_id, 'premiere', dates, matched)
        if show.final is not None:
            find_date_matches(show.final.strftime('%Y-%m-%d'), show.show_id, 'final', dates, matched)

    print(json.dumps(matched, indent=2, sort_keys=True))


for e in E.objects(title__contains='Planet'):
    print(e)
    print(e.title)


years = list(range(1960, 2021))

for y in years:
    from_date = datetime.strptime(str(y) + '-01-01', '%Y-%m-%d')
    to_date = datetime.strptime(str(y) + '-12-31', '%Y-%m-%d')
    ps = Show.objects(premiere__gte=from_date, premiere__lte=to_date)
    premieres = ' | '.join([p.show_id for p in ps])
    fs = Show.objects(final__gte=from_date, final__lte=to_date)
    finals = ' | '.join([f.show_id for f in fs])
    print(y, str(ps.count()).rjust(2), premieres)
    print(y, str(fs.count()).rjust(2), finals)


# find_all_matching_dates()
#
# premieres = Show.objects.aggregate({
#     '$group': {'_id': {'premiere': '$premiere', 'final': '$final'}, 'show_id': {'$push': '$show_id'}}
# })
#
# for p in list(premieres):
#     if len(p['show_id']) > 1:
#         print(p)
#
#
# finals = Show.objects.aggregate({
#     '$group': {'_id': {'final': '$final'}, 'show_id': {'$push': '$show_id'}}
# })
#
# for p in list(finals):
#     if len(p['show_id']) > 1:
#         print(p)
#
#
# print()
#
# years = dict.fromkeys(list(range(1960, 2020)), 0)
#
# for s in Show.objects:
#     for y in years.keys():
#         final = s.final.year if s.final else 2019
#         if s.premiere.year <= y <= final:
#             years[y] += 1
#
# print(years)
# years = dict.fromkeys(list(range(1960, 2021)), 0)
# years_sep = dict.fromkeys(list(range(1960, 2021)), 0)
# print()
# shows = {}
#
# for e in E.objects:
#     if e.air_date:
#         years[e.air_date.year] += 1
#         if not years_sep[e.air_date.year] or e.show_id not in years_sep[e.air_date.year]:
#             years_sep[e.air_date.year] = { e.show_id: 0 }
#
#         years_sep[e.air_date.year][e.show_id] += 1
#
#         if e.show_id not in shows:
#             shows[e.show_id] = dict.fromkeys(list(range(1960, 2021)), 0)
#         shows[e.show_id][e.air_date.year] += 1 if e.episode_option == 'Single' else 2
#
# print(years)
#
# #plt.bar(range(len(years)), list(years.values()), align='center')
# decades = [y if y % 10 == 0 else '' for y in years.keys()]
# plt.xticks(range(len(decades)), list(decades))
#
# #plt.show()
# print(years_sep)
# print(shows)
# df = pd.DataFrame(shows)
#
# df.plot(kind="bar", stacked=True)
# decades = [y if y % 10 == 0 else '' for y in years.keys()]
# plt.xticks(range(len(decades)), list(decades))
# plt.show()

