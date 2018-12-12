from utils.file import File
import unittest
from episode import Episode
from utils.constants import *
from utils.io_utlis import *
from series import Series
import stats
import batch_files
import backup
import restore_backup
import os
import batch_match
import batch_sync
from unlock_shows import unlock
import error_search
from episode import Episode
import file_tree

if not DEBUG:
    print('Debug not on')
    sys.exit(0)

TEST_DATA = load_json('assets/test_data.json')


class E:
    def __init__(self, location='',
                 e_nr=999,
                 s_nr=0,
                 series_name='',
                 episode_option=SINGLE,
                 title='',
                 title2='',
                 title3='',
                 extension='',
                 file_name=''
                 ):

        self.location = location
        self.series_name = series_name
        self.file_name = file_name
        self.extension = extension
        self.s_nr = s_nr
        self.anime = False
        self.episode_option = episode_option
        self.e_nr = e_nr
        self.title = title
        self.title2 = title2
        self.title3 = title3

    def get_title(self):
        title_list = []
        if self.title:
            title_list.append(self.title)
        if not self.episode_option == SINGLE and self.title2:
            title_list.append(self.title2)
        if self.episode_option == TRIPLE and self.title3:
            title_list.append(self.title3)
        return ' & '.join(title_list)

    def id(self):
        return f'{self.series_name} {self.s_nr:02d}x{self.e_nr:0{3 if self.anime else 2}d}'


class TestCompile(unittest.TestCase):
    def test_compiler(self):
        comp_true = TEST_DATA['compile_truth']
        for t1 in ['Brian', '']:
            for t2 in ['Roger', '', 'Brian']:
                for t3 in ['John', '', 'Brian', 'Roger']:
                    for eo in [SINGLE, DOUBLE, TRIPLE]:
                        for a in [True, False]:
                            for se in [[2, 1], [20, 10], [2, 100]]:
                                if se[1] == 100 and not a:
                                    continue
                                f = File(
                                    s_nr=se[0],
                                    e_nr=se[1],
                                    series_name='Freddie',
                                    title=t1,
                                    title2=t2,
                                    title3=t3,
                                    episode_option=eo,
                                    anime=a)
                                f.extension = 'mkv'
                                comp = Episode.compile_file_name(None, f)
                                s = ''.join([t1[0] if t1 else '_', t2[0] if t2 else '_',
                                             t3[0] if t3 else '_', 'A' if a else '_', eo[0],
                                             str(len(str(se[0])) + 3), str(len(str(se[1])))])
                                # print(s)
                                self.assertEqual(comp, comp_true[s])

    def test_parse(self):
        comp_true = TEST_DATA['compile_truth']
        for t1 in ['Brian', '']:
            for t2 in ['Roger', '', 'Brian']:
                for t3 in ['John', '', 'Brian', 'Roger']:
                    for eo in [SINGLE, DOUBLE, TRIPLE]:
                        for a in [True, False]:
                            for se in [[2, 1], [20, 10], [2, 100]]:
                                if se[1] == 100 and not a:
                                    continue
                                s = ''.join([t1[0] if t1 else '_', t2[0] if t2 else '_',
                                             t3[0] if t3 else '_', 'A' if a else '_', eo[0],
                                             str(len(str(se[0])) + 3), str(len(str(se[1])))])
                                # print(s)
                                if s == 'BRJAT41':
                                    pass

                                title1 = t1
                                if not title1 and not eo == SINGLE:
                                    title1 = t2
                                    if not title1 and not eo == DOUBLE:
                                        title1 = t3
                                title2 = ''
                                if not eo == SINGLE:
                                    title2 = t2
                                    if title1 == title2:
                                        title2 = ''
                                    if not title2 and not eo == DOUBLE:
                                        title2 = t3
                                        if title2 == title1:
                                            title2 = ''

                                title3 = t3 if eo == TRIPLE and not title1 == t3 and not title2 == t3 else ''

                                if a:
                                    location = 'L:\\Anime\\Freddie\\Season 02\\' + comp_true[s]
                                else:
                                    location = 'L:\\Series\\Freddie\\Season 02\\' + comp_true[s]
                                e = Episode(location=location)
                                self.assertEqual(e.e_nr, se[1])
                                self.assertEqual(e.s_nr, se[0])
                                self.assertEqual(e.series_name, 'Freddie')
                                self.assertEqual(e.episode_option, eo)
                                self.assertEqual(e.title, title1)
                                self.assertEqual(e.title2, title2)
                                self.assertEqual(e.title3, title3)

    def test_get_title(self):
        file_names = TEST_DATA['compile_truth']
        for t1 in ['Brian', '']:
            for t2 in ['Roger', '', 'Brian']:
                for t3 in ['John', '', 'Brian', 'Roger']:
                    for eo in [SINGLE, DOUBLE, TRIPLE]:
                        for a in [True, False]:
                            for se in [[2, 1], [20, 10], [2, 100]]:
                                if se[1] == 100 and not a:
                                    continue
                                s = ''.join([t1[0] if t1 else '_', t2[0] if t2 else '_',
                                             t3[0] if t3 else '_', 'A' if a else '_', eo[0],
                                             str(len(str(se[0])) + 3), str(len(str(se[1])))])
                                # print(s)

                                file_name = file_names[s]
                                location = os.path.join(ANIME_DIR if a else SERIES_DIR, 'Freddie', 'Season 01', file_name)
                                e = Episode(location=location)
                                title_truth = ''
                                title_split = file_name.split(' - ')
                                if len(title_split) > 1:
                                    title_split = title_split[1].split('.')
                                    if len(title_split) > 1:
                                        title_truth = title_split[0]
                                self.assertEqual(e.get_title(), title_truth)

    def test_sxe(self):
        shows = load_shows(read_only=True)
        battle: Series = shows['Battlestar Galactica']
        self.assertEqual(battle.get_episode_by_sxe(4, 21), battle.get_episode_by_sxe(4, 19))
        self.assertEqual(battle.get_episode_by_sxe(4, 20), battle.get_episode_by_sxe(4, 19))
        self.assertEqual(battle.get_episode_by_sxe(4, 19).e_nr, 19)
        self.assertEqual(battle.get_episode_by_sxe(4, 22), None)
        star: Series = shows['Star Trek - Enterprise']
        self.assertEqual(star.get_episode_by_sxe(1, 2), star.get_episode_by_sxe(1, 1))
        self.assertEqual(star.get_episode_by_sxe(1, 27), None)
        self.assertEqual(star.get_episode_by_sxe(1, 1).e_nr, 1)

    @unittest.skip("takes too long")
    def test_stats(self):
        statistics = stats.main(['--output=stats.json'])
        self.assertTrue(statistics)

    def test_batch_files(self):
        clean_file_dir()
        create_batch_tree()
        files = batch_files.main(['--output=batch_files_out.json'])
        self.maxDiff = None
        self.assertDictEqual(files, TEST_DATA['batch_files_truth'])

        #clean_file_dir()

    def test_batch_match(self):
        clean_file_dir()
        create_batch_tree()
        conf_file = 'data/batch_match_test_conf.json'
        save_json(TEST_DATA['batch_match_conf'], conf_file)
        output = batch_match.main(
            [''.join(['--config=', os.path.basename(conf_file)]), '--output=batch_match_out.json'])
        self.maxDiff = None
        self.assertDictEqual(output, TEST_DATA['batch_match_truth'])
        clean_file_dir()

    def test_batch_sync(self):
        recursive_delete(os.path.join(SERIES_DIR, 'Castle'))
        clean_file_dir()
        create_batch_tree()
        conf_file = 'data/batch_sync_test_conf.json'
        save_json(TEST_DATA['batch_sync_conf'], conf_file)
        output = batch_sync.main(
            [''.join(['--config=', os.path.basename(conf_file)]), '--output=batch_sync_out.json'])
        self.maxDiff = None
        self.assertDictEqual(output, TEST_DATA['batch_sync_truth'])
        self.assertEqual(len(os.listdir(FILE_DIR)), 2)

        shows = load_shows()
        show: Series = shows.pop('Castle')
        self.assertEqual(show.anime, False)
        self.assertEqual(show.final, '')
        self.assertEqual(show.name_needed, True)
        self.assertEqual(show.premiere, '2009-03-09')
        self.assertEqual(show.series_name, 'Castle')
        self.assertEqual(show.status, ENDED)
        self.assertEqual(show.tvdb_id, 83462)
        count = 0
        names = {
            1: {1: 'Castle 01x01.mkv'},
            2: {2: 'Castle 02x02 & 02x03 - The Double Down & Inventing the Girl.mkv'},
            4: {4: 'Castle 04x04 & 04x05 & 04x06 - Kick the Ballistics & Eye of the Beholder & Demons.mkv'}
        }
        for s in show.seasons.values():
            for e in s.episodes.values():
                count += 1
                self.assertTrue(os.path.isfile(e.location))
                self.assertEqual(e.compile_file_name(), names[e.s_nr][e.e_nr])
        self.assertEqual(count, 3)

        clean_file_dir()
        recursive_delete(show.location)
        save_shows(shows)

    def test_error_search(self):
        show = Series(series_name='Tiny Dancer')

        e1 = E(location='',
               e_nr=1,
               s_nr=1,
               series_name='',
               episode_option=SINGLE,
               title='Blues & d\'Etat Part I',
               title2='',
               title3='')
        show.add_episode(e1)

        e2 = E(location='',
               e_nr=2,
               s_nr=1,
               series_name='',
               episode_option=SINGLE,
               title='a Hand Above',
               title2='',
               title3='')
        show.add_episode(e2)

        e3 = E(location='',
               e_nr=3,
               s_nr=1,
               series_name='',
               episode_option=DOUBLE,
               title='Grace another Table',
               title2='Raise Our Glasses Part IIIII',
               title3='')
        show.add_episode(e3)

        e4 = E(location='',
               e_nr=4,
               s_nr=1,
               series_name='',
               episode_option=SINGLE,
               title='Raise The Glasses Part 9',
               title2='',
               title3='')
        show.add_episode(e4)

        e5 = E(location='',
               e_nr=5,
               s_nr=1,
               series_name='',
               episode_option=DOUBLE,
               title='Programmed to Receive Part I and Part I',
               title2='',
               title3='')
        show.add_episode(e5)

        e6 = E(location='',
               e_nr=6,
               s_nr=1,
               series_name='',
               episode_option=SINGLE,
               title='Raise The Glasses Part I',
               title2='',
               title3='')
        show.add_episode(e6)

        e7 = E(location='',
               e_nr=999,
               s_nr=1,
               series_name='Tiny Dancer',
               episode_option=SINGLE,
               title='Tiny Dancer - Programmed to  Receive Part II',
               title2='',
               title3='',
               file_name='Tiny Dancer 01x - Programmed to  Receive Part II')
        show.add_episode(e7)

        e8 = E(location='',
               e_nr=8,
               s_nr=1,
               series_name='',
               episode_option=SINGLE,
               title='Dancing @ the Sand ',
               title2='',
               title3='',
               file_name='Tiny Dancer 01x08 - Dancing in the Sand .mkv')
        show.add_episode(e8)

        e9 = E(location='',
               e_nr=9,
               s_nr=1,
               series_name='',
               episode_option=SINGLE,
               title='Dancing @ the Sand ',
               title2='',
               title3='',
               file_name='Tiny Dancer 02x08 - Dancing in the Sand .mkv')
        show.add_episode(e9)

        e10 = E(location='',
                e_nr=10,
                s_nr=1,
                series_name='',
                episode_option=SINGLE,
                title='',
                title2='',
                title3='',
                file_name='Sensation 01x10 - In the Year.mkv',
                extension='avi')
        show.add_episode(e10)

        e11 = E(location='',
                e_nr=11,
                s_nr=1,
                series_name='',
                episode_option=SINGLE,
                title='',
                title2='',
                title3='',
                file_name='Sensation 01x10 - In the Year.mkv',
                extension='txt')
        show.add_episode(e11)

        errors = []
        true = TEST_DATA['error_truth']
        errors.append(error_search.check_words(show, e1))
        errors.append(error_search.check_words(show, e2))
        errors.append(error_search.check_words(show, e3))
        errors.append(error_search.check_words(show, e4))
        errors.append(error_search.check_words(show, e7))

        errors.append(error_search.check_part_number(show, e1))
        errors.append(error_search.check_part_number(show, e3))
        errors.append(error_search.check_part_number(show, e4))
        errors.append(error_search.check_part_number(show, e5))
        errors.append(error_search.check_part_number(show, e6))
        errors.append(error_search.check_part_number(show, e7))

        errors.append(error_search.check_part_number(show, e6))
        errors.append(error_search.check_for_spaces(show, e7))
        errors.append(error_search.check_for_spaces(show, e8))

        errors.append(error_search.check_for_missing_title(show, e6))
        errors.append(error_search.check_for_missing_title(show, e9))
        show.name_needed = True
        errors.append(error_search.check_for_missing_title(show, e9))

        errors.append(error_search.check_symbols(show, e7))
        errors.append(error_search.check_symbols(show, e8))

        errors.append(error_search.check_series_name_and_numbers(show, e7))
        errors.append(error_search.check_series_name_and_numbers(show, e8))
        errors.append(error_search.check_series_name_and_numbers(show, e9))
        errors.append(error_search.check_series_name_and_numbers(show, e10))

        errors.append(error_search.check_for_multiple_files(show, e3))
        errors.append(error_search.check_for_multiple_files(show, e4))

        errors.append(error_search.check_for_name_used_twice(show, e8))
        errors.append(error_search.check_for_name_used_twice(show, e9))

        errors.append(error_search.check_extension(show, e8))
        errors.append(error_search.check_extension(show, e11))
        errors.append(error_search.check_extension(show, e10))

        self.maxDiff = None
        for t, e in zip(true, errors):
            if not type(t) is dict:
                self.assertEqual(e, t)
            else:
                self.assertDictEqual(e, t)

    def test_file_tree(self):
        date = backup.main()
        shows = pickle_load('data/test_shows.pkl')
        save_shows(shows)
        tree = file_tree.main()

        restore_backup.main(date=date)
        recursive_delete(os.path.join(BACKUP_DIR, date))


def clean_file_dir():
    recursive_delete(FILE_DIR)
    wait_on_delete(FILE_DIR)
    os.makedirs(FILE_DIR)


def create_batch_tree():
    tree = [FILE_DIR,
            ['season 01', '01x01.mkv', 's02e02.mkv', 's03e03.txt', ['subs', 's02e02.srt', 's03e03.srt']],
            '04x04.mkv',
            '0505.avi',
            '06.txt'
            ]
    create_tree(tree)


def create_tree(tree):
    root = tree[0]
    try:
        os.mkdir(root)
    except FileExistsError:
        pass
    wait_on_creation(root)
    for item in tree[1:]:
        if type(item) is str:
            f = open(os.path.join(root, item), 'w+')
            f.close()
        else:
            item[0] = os.path.join(root, item[0])
            create_tree(item)




