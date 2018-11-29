import io_utlis
import time
import sys
from error_search import *

SHOWS = None
MISSING = []


def main(args=None, series_name='*', out_file='data/treefile_comb'):
    global SHOWS
    SHOWS = io_utlis.load_shows(read_only=True)
    if args:
        io_utlis.parse_args(args)
        conf = io_utlis.load_json(os.environ["CONF_FILE"])
        series_name = conf[SERIES_NAME]
        out_file = os.environ['OUTPUT_FILE']

    if SHOWS is None:
        io_utlis.save_json({'shows_locked': True}, out_file)
        print('shows locked')
        return

    if series_name == '*':
        tree_file = load_all()
    else:
        tree_file = io_utlis.load_json(out_file)

        show, error = get_show_data(SHOWS[series_name])
        for i in range(len(tree_file['errors'])):
            if tree_file['errors'][i][SERIES_NAME] == series_name:
                if error:
                    tree_file['errors'][i] = error
                else:
                    del tree_file['errors'][i]
                break
        tree_file['shows'][series_name] = show
    io_utlis.save_json(tree_file, out_file)
    io_utlis.save_shows(SHOWS)


def load_all():
    tree = {}
    errors = []
    for show in SHOWS.values():
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
            error = check_for_empty_season(show, season)
        sea = {'key': season.s_nr, 'episodes': [], 'opened': False}
        episodes = sorted(list(season.episodes.values()), key=lambda x: x.e_nr)
        for episode in episodes:
            if not error:
                error = check_for_spaces(show, episode)
            if not error:
                error = check_extension(show, episode)
            if not error:
                error = check_part_number(show, episode)
            if not error:
                error = check_words(show, episode)
            if not error:
                error = check_symbols(show, episode)
            if not error:
                error = check_series_name_and_numbers(show, episode)
            if not error:
                error = check_for_missing_title(show, episode)
            if not error:
                error = check_for_multiple_files(show, episode)
            if not error:
                error = check_for_name_used_twice(show, episode)


            if not error:
                error = check_against_compiled(show, episode)

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


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1:])
    print(time.time() - start)
