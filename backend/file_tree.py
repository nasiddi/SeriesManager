from sys import argv
from os import environ

import error_search
from io_utlis import load_shows, parse_args, save_json, save_shows, load_json
from constants import CONF_FILE, OUT_FILE, SERIES_NAME, LOCATION

SHOWS = None
MISSING = []


def main(args=None, series_name='*', out_file='data/tree_file_comb'):
    global SHOWS
    SHOWS = load_shows(read_only=True)
    if args:
        parse_args(args)
        conf = load_json(environ[CONF_FILE])
        series_name = conf[SERIES_NAME]
        out_file = environ[OUT_FILE]

    if series_name == '*':
        tree_file = load_all()
    else:
        tree_file = load_json(out_file)

        show, error = get_show_data(SHOWS[series_name])
        for i in range(len(tree_file['errors'])):
            if tree_file['errors'][i][SERIES_NAME] == series_name:
                if error:
                    tree_file['errors'][i] = error
                else:
                    del tree_file['errors'][i]
                break
        tree_file['shows'][series_name] = show
    save_json(tree_file, out_file)
    save_shows(SHOWS)


def load_all():
    tree = {}
    errors = []
    for show in sorted(SHOWS.values(), key=get_series_name):
        show_tree, show_error = get_show_data(show)
        tree[show.series_name] = show_tree
        if show_error:
            errors.append(show_error)
    return {'shows': tree, 'errors': errors, 'info': 'Tree is Clean'}


def get_show_data(show):
    seasons = []
    error = None
    for season in show.seasons.values():
        if not error:
            error = error_search.check_for_empty_season(show, season)
        sea = {'key': season.s_nr, 'episodes': [], 'opened': False}
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            if not error:
                error = error_search.check_for_spaces(show, episode)
            if not error:
                error = error_search.check_extension(show, episode)
            if not error:
                error = error_search.check_part_number(show, episode)
            if not error:
                error = error_search.check_words(show, episode)
            if not error:
                error = error_search.check_symbols(show, episode)
            if not error:
                error = error_search.check_series_name_and_numbers(show, episode)
            if not error:
                error = error_search.check_for_missing_title(show, episode)
            if not error:
                error = error_search.check_for_multiple_files(show, episode)
            if not error:
                error = error_search.check_for_name_used_twice(show, episode)

            if not error:
                error = error_search.check_against_compiled(show, episode)

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
    return {SERIES_NAME: show.series_name, 'seasons': seasons}, error


def get_series_name(show):
    return show.series_name


if __name__ == '__main__':
    main(argv[1:])
