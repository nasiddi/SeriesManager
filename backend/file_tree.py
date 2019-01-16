from os import environ
from sys import argv

import error_search
from utils.constants import OUT_FILE, SERIES_NAME, LOCATION
from utils.io_utlis import load_shows, parse_args, save_json, save_shows

SHOWS = None
MISSING = []


def main(args=None, out_file='data/tree_file_comb.json'):
    global SHOWS
    SHOWS = load_shows(read_only=True)
    if args:
        parse_args(args)
        out_file = environ[OUT_FILE]

    tree_file = load_all()

    save_json(tree_file, out_file)
    save_shows(SHOWS)
    return tree_file


def load_all():
    tree = {}
    errors = []
    for show in sorted(SHOWS.values(), key=get_series_name):
        show_tree, show_error = get_show_data(show, len(errors) < 100)
        tree[show.series_name] = show_tree
        if show_error:
            if type(show_error) == list:
                errors.extend(show_error)
            else:
                errors.append(show_error)
    return {'shows': tree, 'errors': errors, 'info': 'Tree is Clean'}


def get_show_data(show, get_errors):
    print(show.series_name)
    seasons = []
    error = None
    error_search.load_data_from_db(show)
    for season in show.seasons.values():
        if not error and get_errors:
            error = error_search.check_for_empty_season(show, season)
        sea = {'key': season.s_nr, 'episodes': [], 'opened': False}
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            if not error and get_errors:
                error = error_search.check_for_spaces(show, episode)
            if not error and get_errors:
                error = error_search.check_extension(show, episode)
            if not error and get_errors:
                error = error_search.check_part_number(show, episode)
            if not error and get_errors:
                error = error_search.check_words(show, episode)
            if not error and get_errors:
                error = error_search.check_symbols(show, episode)
            if not error and get_errors:
                error = error_search.check_series_name_and_numbers(show, episode)
            if not error and get_errors:
                error = error_search.check_for_missing_title(show, episode)
            if not error and get_errors:
                error = error_search.check_for_multiple_files(show, episode)
            if not error and get_errors:
                error = error_search.check_for_name_used_twice(show, episode)

            if not error and get_errors:
                error = error_search.check_against_compiled(show, episode)
            if not error and get_errors:
                error = error_search.check_title_against_db(show, episode)

            sea['episodes'].append({LOCATION: episode.location,
                                    'file_name': episode.file_name,
                                    'e_nr': episode.e_nr,
                                    's_nr': episode.s_nr,
                                    'e_nr_old': episode.e_nr,
                                    's_nr_old': episode.s_nr,
                                    'title': episode.title,
                                    'title2': episode.title2,
                                    'title3': episode.title3,
                                    'extension': episode.extension,
                                    'save': False,
                                    'delete': False,
                                    'episode_option': episode.episode_option,
                                    'size': episode.size,
                                    'duration': episode.duration,
                                    'quality': episode.quality,
                                    'tvdb_id': show.tvdb_id,
                                    'name_needed': show.name_needed})

        seasons.append(sea)
    if error:
        print(error)
    return {SERIES_NAME: show.series_name, 'seasons': seasons}, error


def get_series_name(show):
    return show.series_name


if __name__ == '__main__':
    main(argv[1:])
