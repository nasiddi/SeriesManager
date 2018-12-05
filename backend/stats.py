from json import loads
from math import gcd
from os import environ, path
from shlex import split
from subprocess import check_output
from sys import argv, stderr
from time import time

from utils.constants import SERIES_NAME, SINGLE, DOUBLE, ASPECT_RATIOS, QUALITY, OUT_FILE
from utils.io_utlis import load_shows, parse_args, save_json

SHOWS = None


def main(args):
    global SHOWS
    SHOWS = load_shows(read_only=True)
    parse_args(args)

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

                if episode.duration == 0 or episode.quality == '':
                    update_file_meta(episode)

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

        print(show.series_name)

        show_stats['avg_duration'] = int(show_stats['duration'] / show_stats['episodes'] * 100) / 100.0
        show_stats['avg_size'] = int(show_stats['size'] / show_stats['episodes'] * 100) / 100.0
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

    save_json(stats, environ[OUT_FILE])


def update_file_meta(episode):
    data = find_video_metada(episode.location)
    if data:
        episode.set_file_meta(data)

    if episode.height == 0 or episode.width == 0:
        ratio = 0
    else:
        ratio = int(1000.0 * episode.width / episode.height) / 1000.0
        ratio = min(ASPECT_RATIOS, key=lambda x: abs(x-ratio))
    episode.ratio = ratio
    if episode.height == 0:
        episode.quality = ''
    else:
        episode.quality = QUALITY[min(QUALITY, key=lambda x: abs(x-episode.height))]


def find_video_metada(file):
    cmd = "ffprobe -v quiet -print_format json -show_streams -show_format -i"
    args = split(cmd)
    args.append(file)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    try:
        ffprobe_output = check_output(args).decode('utf-8')
    except Exception as e:
        print(path.basename(file), file=stderr)
        print(e, file=stderr)
        return None
    ffprobe_output = loads(ffprobe_output)

    # prints all the metadata available:
    # import pprint
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(ffprobe_output)

    height = 0
    width = 0
    duration = 0
    size = 0
    ratio = ''
    # for example, find height and width
    video_stream = None
    for stream in ffprobe_output['streams']:
        if 'codec_type' in stream and stream['codec_type'] == 'video':
            video_stream = stream
            break
    try:
        height = video_stream['height']
    except:
        pass
    try:
        width = video_stream['width']
    except:
        pass
    try:
        duration = int(float(ffprobe_output['format']['duration']) / 60 * 100) / 100.0
    except:
        pass
    try:
        size = int(float(ffprobe_output['format']['size']) / 1024.0 / 1024.0 * 100) / 100.0
    except:
        pass
    try:
        ratio = video_stream['display_aspect_ratio']
    except:
        if not height == 0 and not width == 0:
            d = gcd(width, height)
            ratio = str(int(width/d)) + ':' + str(int(height/d))

    # print(os.path.basename(file))
    # print('height', height, 'pixel')
    # print('size:', size, 'MB')
    # print('duration', duration, 'minutes')
    # print('ratio', ratio)
    # print('*************************')
    return height, width, size, duration, ratio


if __name__ == '__main__':
    start = time()
    main(argv[1:])
    print(time() - start)
