from os import environ
from sys import argv
from time import time

from utils.constants import SERIES_NAME, SINGLE, DOUBLE, ASPECT_RATIOS, OUT_FILE, DEBUG, AIRING
from utils.io_utlis import load_shows, parse_args, save_json

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = load_shows(read_only=True)
    parse_args(args)
    print(environ[OUT_FILE])
    stats = {'shows': [], 'status': [], 'extension': [], 'ratio': [], 'quality': []}
    for show in SHOWS.values():
        show_stats = {SERIES_NAME: show.series_name, 'status': {show.status: 1}, 'premiere': show.premiere, 'avg_e_per_s': 0,
                      'final': show.final, 'ratio': {}, 'extension': {}, 'duration': 0, 'episodes': 0, 'genre1': show.genre1, 'genre2': show.genre2,
                      'seasons': 0, 'size': 0, 'quality': {}, 'selected': '', 'color': '', 'result': False}

        if show.status not in stats['status']:
            stats['status'].append(show.status)

        for season in show.seasons.values():
            show_stats['seasons'] += 1

            if not season.s_nr >= len(list(show.seasons.values())) or not show.status == AIRING:
                show_stats['avg_e_per_s'] += len(season.episode_numbers)
            for episode in season.episodes.values():
                episode_option = 1 if episode.episode_option == SINGLE else 2 if episode.episode_option == DOUBLE else 3

                if not DEBUG and episode.duration == 0 or episode.quality == '':
                    episode.update_file_meta()

                show_stats['duration'] += episode.duration
                show_stats['episodes'] += episode_option
                show_stats['size'] += episode.size

                if episode.extension not in stats['extension']:
                    stats['extension'].append(episode.extension)
                if episode.extension in show_stats['extension']:
                    show_stats['extension'][episode.extension] += episode_option
                else:
                    show_stats['extension'][episode.extension] = episode_option

                if episode.quality not in stats['quality']:
                    stats['quality'].append(episode.quality)
                if episode.quality in show_stats['quality']:
                    show_stats['quality'][episode.quality] += episode_option
                else:
                    show_stats['quality'][episode.quality] = episode_option

                if episode.ratio not in stats['ratio']:
                    stats['ratio'].append(episode.ratio)
                if episode.ratio in show_stats['ratio']:
                    show_stats['ratio'][episode.ratio] += episode_option
                else:
                    show_stats['ratio'][episode.ratio] = episode_option

        keys = list(show_stats['ratio'].keys())
        for key in keys:
            try:
                show_stats['ratio'][ASPECT_RATIOS[key]] = show_stats['ratio'][key]
            except:
                pass
            finally:
                show_stats['ratio'].pop(key, None)

        if show_stats['episodes']:
            show_stats['avg_duration'] = int(show_stats['duration'] / show_stats['episodes'] * 100) / 100.0
            show_stats['avg_size'] = int(show_stats['size'] / show_stats['episodes'] * 100) / 100.0
        else:
            show_stats['avg_duration'] = 0
            show_stats['avg_size'] = 0

        show_stats['duration'] = int(show_stats['duration'] / 60.0 * 100) / 100.0
        show_stats['size'] = int(show_stats['size'] / 1024.0 * 100) / 100.0
        try:
            show_stats['avg_e_per_s'] = int(show_stats['avg_e_per_s'] / (show_stats['seasons'] if not show.status == AIRING else show_stats['seasons'] - 1) * 100) / 100.0
        except ZeroDivisionError:
            pass
        stats['shows'].append(show_stats)

    temp = []
    for key in stats['ratio']:
        try:
            temp.append(ASPECT_RATIOS[key])
        except:
            pass
    stats['ratio'] = temp

    save_json(stats, environ[OUT_FILE])
    return stats


if __name__ == '__main__':
    start = time()
    main(argv[1:])
    print(time() - start)
