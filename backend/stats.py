from os import environ
from sys import argv
from time import time

from utils.constants import SERIES_NAME, SINGLE, DOUBLE, ASPECT_RATIOS, OUT_FILE, DEBUG
from utils.io_utlis import load_shows, parse_args, save_json

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = load_shows(read_only=True)
    parse_args(args)
    print(environ[OUT_FILE])
    stats = {'shows': [], 'total': {'status': {}, 'extension': {}, 'ratio': {}, 'quality': {}}}
    duration = 0
    show_count = 0
    sea_count = 0
    ep_count = 0
    size = 0
    for show in SHOWS.values():
        show_count += 1
        show_stats = {SERIES_NAME: show.series_name, 'status': {show.status: 1}, 'premiere': show.premiere,
                      'final': show.final, 'ratio': {}, 'extension': {}, 'duration': 0, 'episodes': 0,
                      'seasons': 0, 'size': 0, 'quality': {}}

        if show.status in stats['total']['status']:
            stats['total']['status'][show.status] += 1
        else:
            stats['total']['status'][show.status] = 1

        for season in show.seasons.values():
            sea_count += 1
            show_stats['seasons'] += 1

            for episode in season.episodes.values():
                episode_option = 1 if episode.episode_option == SINGLE else 2 if episode.episode_option == DOUBLE else 3

                if not DEBUG and episode.duration == 0 or episode.quality == '':
                    episode.update_file_meta()

                duration += episode.duration
                show_stats['duration'] += episode.duration
                ep_count += episode_option
                show_stats['episodes'] += episode_option
                size += episode.size
                show_stats['size'] += episode.size

                if episode.extension in stats['total']['extension']:
                    stats['total']['extension'][episode.extension] += episode_option
                else:
                    stats['total']['extension'][episode.extension] = episode_option
                if episode.extension in show_stats['extension']:
                    show_stats['extension'][episode.extension] += episode_option
                else:
                    show_stats['extension'][episode.extension] = episode_option

                if episode.quality in stats['total']['quality']:
                    stats['total']['quality'][episode.quality] += episode_option
                else:
                    stats['total']['quality'][episode.quality] = episode_option
                if episode.quality in show_stats['quality']:
                    show_stats['quality'][episode.quality] += episode_option
                else:
                    show_stats['quality'][episode.quality] = episode_option

                if episode.ratio in stats['total']['ratio']:
                    stats['total']['ratio'][episode.ratio] += episode_option
                else:
                    stats['total']['ratio'][episode.ratio] = episode_option

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
        stats['shows'].append(show_stats)

    keys = list(stats['total']['ratio'].keys())
    for key in keys:
        try:
            stats['total']['ratio'][ASPECT_RATIOS[key]] = stats['total']['ratio'][key]
            stats['total']['ratio'].pop(key, None)
        except KeyError:
            pass

    keys = list(stats['total']['extension'].keys())
    stats['extensions'] = keys
    stats['total']['extension'].update({'other': 0})
    for key in keys:
        try:
            if stats['total']['extension'][key] < 1000:
                stats['total']['extension']['other'] += stats['total']['extension'][key]
                stats['total']['extension'].pop(key, None)
        except KeyError:
            pass

    stats['total']['days'] = int(duration / 60.0 / 24.0 * 100) / 100.0
    stats['total']['hours'] = int(duration / 60.0 * 100) / 100.0

    stats['total']['eps'] = ep_count
    stats['total']['seas'] = sea_count
    stats['total']['shows'] = show_count

    stats['total']['tb'] = int(size / 1024.0 / 1024.0 * 100) / 100.0
    stats['total']['gb'] = int(size / 1024.0 * 100) / 100.0

    stats['total']['avg_sea_show'] = int(sea_count / show_count * 100.0) / 100.0
    stats['total']['avg_ep_sea'] = int(ep_count / sea_count * 100.0) / 100.0
    stats['total']['avg_ep_show'] = int(ep_count / show_count * 100.0) / 100.0
    stats['total']['avg_duration_ep'] = int(duration / ep_count * 100.0) / 100.0
    stats['total']['avg_duration_show'] = int(duration / show_count / 60.0 * 100.0) / 100.0

    stats['total']['avg_mb_ep'] = int(size / ep_count * 100.0) / 100.0
    stats['total']['avg_gb_show'] = int(size / show_count / 1024 * 100.0) / 100.0
    for s in stats['shows']:
        keys = s['quality'].keys()
        for k in keys:
            if type(k) is int:
                print(s['series_name'])

    save_json(stats, environ[OUT_FILE])
    return stats

if __name__ == '__main__':
    start = time()
    main(argv[1:])
    print(time() - start)
