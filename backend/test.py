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

windows = platform.system() == 'Windows'
SERIES_DIR = 'L:\\Series' if windows else '/Volumes/Downloads/Series'
ANIME_DIR = 'L:\\Anime' if windows else '/Volumes/Downloads/Anime'
HD_Movies = 'L:\\HD' if windows else '/Volumes/Downloads/HD'
SD_MOVIES = 'L:\\SD' if windows else '/Volumes/Downloads/SD'
FILE_DIR = 'L:\\complete\\' if windows else '/Volumes/Downloads/complete/'
SUB_DIR = 'T:\\Subs' if windows else '/Volumes/Temp/Subs'
MAC_OFFSET = 0 if windows else 2


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
        if not self.title:
            return ''
        if self.episode_option == DOUBLE:
            if self.title2:
                return ' & '.join([self.title, self.title2])
        elif self.episode_option == TRIPLE:
            if self.title2 and self.title3:
                return ' & '.join([self.title, self.title2, self.title3])
        return self.title

    def id(self):
        return f'{self.series_name} {self.s_nr:02d}x{self.e_nr:0{3 if self.anime else 2}d}'


class TestCompile(unittest.TestCase):
    def test_compiler(self):
        comp_true = get_compile_truth()
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
        comp_true = get_compile_truth()
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
        self.assertDictEqual(files, get_batch_files_truth())

        clean_file_dir()

    def test_batch_match(self):
        clean_file_dir()
        create_batch_tree()
        conf_file = 'data/batch_match_test_conf.json'
        save_json(get_batch_match_conf(), conf_file)
        output = batch_match.main(
            [''.join(['--config=', os.path.basename(conf_file)]), '--output=batch_match_out.json'])
        self.maxDiff = None
        self.assertDictEqual(output, get_batch_match_truth())
        clean_file_dir()

    def test_batch_sync(self):
        recursive_delete(os.path.join(SERIES_DIR, 'Castle'))
        clean_file_dir()
        create_batch_tree()
        conf_file = 'data/batch_sync_test_conf.json'
        save_json(get_batch_sync_conf(), conf_file)
        output = batch_sync.main(
            [''.join(['--config=', os.path.basename(conf_file)]), '--output=batch_sync_out.json'])
        self.maxDiff = None
        self.assertDictEqual(output, get_batch_sync_truth())
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
               title='',
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
               file_name='Sensation 01x10 - In the Year.mkv')
        show.add_episode(e10)



        errors = []
        true = get_error_truth()
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

        print(json.dumps(errors, indent=4, sort_keys=True))
        print(errors)

        self.maxDiff = None
        for t, e in zip(true, errors):
            if not type(t) is dict:
                self.assertEqual(e, t)
            else:
                self.assertDictEqual(e, t)

        print(show.seasons[1].episode_numbers)


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


def get_compile_truth():
    return {
        'BRJAS41': 'Freddie 02x001 - Brian.mkv',
        'BRJAS52': 'Freddie 20x010 - Brian.mkv',
        'BRJAS43': 'Freddie 02x100 - Brian.mkv',
        'BRJ_S41': 'Freddie 02x01 - Brian.mkv',
        'BRJ_S52': 'Freddie 20x10 - Brian.mkv',
        'BRJAD41': 'Freddie 02x001 & 02x002 - Brian & Roger.mkv',
        'BRJAD52': 'Freddie 20x010 & 20x011 - Brian & Roger.mkv',
        'BRJAD43': 'Freddie 02x100 & 02x101 - Brian & Roger.mkv',
        'BRJ_D41': 'Freddie 02x01 & 02x02 - Brian & Roger.mkv',
        'BRJ_D52': 'Freddie 20x10 & 20x11 - Brian & Roger.mkv',
        'BRJAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger & John.mkv',
        'BRJAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger & John.mkv',
        'BRJAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger & John.mkv',
        'BRJ_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger & John.mkv',
        'BRJ_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger & John.mkv',
        'BR_AS41': 'Freddie 02x001 - Brian.mkv',
        'BR_AS52': 'Freddie 20x010 - Brian.mkv',
        'BR_AS43': 'Freddie 02x100 - Brian.mkv',
        'BR__S41': 'Freddie 02x01 - Brian.mkv',
        'BR__S52': 'Freddie 20x10 - Brian.mkv',
        'BR_AD41': 'Freddie 02x001 & 02x002 - Brian & Roger.mkv',
        'BR_AD52': 'Freddie 20x010 & 20x011 - Brian & Roger.mkv',
        'BR_AD43': 'Freddie 02x100 & 02x101 - Brian & Roger.mkv',
        'BR__D41': 'Freddie 02x01 & 02x02 - Brian & Roger.mkv',
        'BR__D52': 'Freddie 20x10 & 20x11 - Brian & Roger.mkv',
        'BR_AT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger.mkv',
        'BR_AT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger.mkv',
        'BR_AT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger.mkv',
        'BR__T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger.mkv',
        'BR__T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger.mkv',
        'BRBAS41': 'Freddie 02x001 - Brian.mkv',
        'BRBAS52': 'Freddie 20x010 - Brian.mkv',
        'BRBAS43': 'Freddie 02x100 - Brian.mkv',
        'BRB_S41': 'Freddie 02x01 - Brian.mkv',
        'BRB_S52': 'Freddie 20x10 - Brian.mkv',
        'BRBAD41': 'Freddie 02x001 & 02x002 - Brian & Roger.mkv',
        'BRBAD52': 'Freddie 20x010 & 20x011 - Brian & Roger.mkv',
        'BRBAD43': 'Freddie 02x100 & 02x101 - Brian & Roger.mkv',
        'BRB_D41': 'Freddie 02x01 & 02x02 - Brian & Roger.mkv',
        'BRB_D52': 'Freddie 20x10 & 20x11 - Brian & Roger.mkv',
        'BRBAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger.mkv',
        'BRBAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger.mkv',
        'BRBAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger.mkv',
        'BRB_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger.mkv',
        'BRB_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger.mkv',
        'BRRAS41': 'Freddie 02x001 - Brian.mkv',
        'BRRAS52': 'Freddie 20x010 - Brian.mkv',
        'BRRAS43': 'Freddie 02x100 - Brian.mkv',
        'BRR_S41': 'Freddie 02x01 - Brian.mkv',
        'BRR_S52': 'Freddie 20x10 - Brian.mkv',
        'BRRAD41': 'Freddie 02x001 & 02x002 - Brian & Roger.mkv',
        'BRRAD52': 'Freddie 20x010 & 20x011 - Brian & Roger.mkv',
        'BRRAD43': 'Freddie 02x100 & 02x101 - Brian & Roger.mkv',
        'BRR_D41': 'Freddie 02x01 & 02x02 - Brian & Roger.mkv',
        'BRR_D52': 'Freddie 20x10 & 20x11 - Brian & Roger.mkv',
        'BRRAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger.mkv',
        'BRRAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger.mkv',
        'BRRAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger.mkv',
        'BRR_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger.mkv',
        'BRR_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger.mkv',
        'B_JAS41': 'Freddie 02x001 - Brian.mkv',
        'B_JAS52': 'Freddie 20x010 - Brian.mkv',
        'B_JAS43': 'Freddie 02x100 - Brian.mkv',
        'B_J_S41': 'Freddie 02x01 - Brian.mkv',
        'B_J_S52': 'Freddie 20x10 - Brian.mkv',
        'B_JAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'B_JAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'B_JAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'B_J_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'B_J_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'B_JAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & John.mkv',
        'B_JAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & John.mkv',
        'B_JAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & John.mkv',
        'B_J_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & John.mkv',
        'B_J_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & John.mkv',
        'B__AS41': 'Freddie 02x001 - Brian.mkv',
        'B__AS52': 'Freddie 20x010 - Brian.mkv',
        'B__AS43': 'Freddie 02x100 - Brian.mkv',
        'B___S41': 'Freddie 02x01 - Brian.mkv',
        'B___S52': 'Freddie 20x10 - Brian.mkv',
        'B__AD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'B__AD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'B__AD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'B___D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'B___D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'B__AT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        'B__AT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        'B__AT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        'B___T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        'B___T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        'B_BAS41': 'Freddie 02x001 - Brian.mkv',
        'B_BAS52': 'Freddie 20x010 - Brian.mkv',
        'B_BAS43': 'Freddie 02x100 - Brian.mkv',
        'B_B_S41': 'Freddie 02x01 - Brian.mkv',
        'B_B_S52': 'Freddie 20x10 - Brian.mkv',
        'B_BAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'B_BAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'B_BAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'B_B_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'B_B_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'B_BAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        'B_BAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        'B_BAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        'B_B_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        'B_B_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        'B_RAS41': 'Freddie 02x001 - Brian.mkv',
        'B_RAS52': 'Freddie 20x010 - Brian.mkv',
        'B_RAS43': 'Freddie 02x100 - Brian.mkv',
        'B_R_S41': 'Freddie 02x01 - Brian.mkv',
        'B_R_S52': 'Freddie 20x10 - Brian.mkv',
        'B_RAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'B_RAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'B_RAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'B_R_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'B_R_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'B_RAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger.mkv',
        'B_RAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger.mkv',
        'B_RAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger.mkv',
        'B_R_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger.mkv',
        'B_R_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger.mkv',
        'BBJAS41': 'Freddie 02x001 - Brian.mkv',
        'BBJAS52': 'Freddie 20x010 - Brian.mkv',
        'BBJAS43': 'Freddie 02x100 - Brian.mkv',
        'BBJ_S41': 'Freddie 02x01 - Brian.mkv',
        'BBJ_S52': 'Freddie 20x10 - Brian.mkv',
        'BBJAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'BBJAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'BBJAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'BBJ_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'BBJ_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'BBJAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & John.mkv',
        'BBJAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & John.mkv',
        'BBJAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & John.mkv',
        'BBJ_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & John.mkv',
        'BBJ_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & John.mkv',
        'BB_AS41': 'Freddie 02x001 - Brian.mkv',
        'BB_AS52': 'Freddie 20x010 - Brian.mkv',
        'BB_AS43': 'Freddie 02x100 - Brian.mkv',
        'BB__S41': 'Freddie 02x01 - Brian.mkv',
        'BB__S52': 'Freddie 20x10 - Brian.mkv',
        'BB_AD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'BB_AD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'BB_AD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'BB__D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'BB__D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'BB_AT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        'BB_AT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        'BB_AT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        'BB__T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        'BB__T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        'BBBAS41': 'Freddie 02x001 - Brian.mkv',
        'BBBAS52': 'Freddie 20x010 - Brian.mkv',
        'BBBAS43': 'Freddie 02x100 - Brian.mkv',
        'BBB_S41': 'Freddie 02x01 - Brian.mkv',
        'BBB_S52': 'Freddie 20x10 - Brian.mkv',
        'BBBAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'BBBAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'BBBAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'BBB_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'BBB_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'BBBAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        'BBBAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        'BBBAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        'BBB_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        'BBB_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        'BBRAS41': 'Freddie 02x001 - Brian.mkv',
        'BBRAS52': 'Freddie 20x010 - Brian.mkv',
        'BBRAS43': 'Freddie 02x100 - Brian.mkv',
        'BBR_S41': 'Freddie 02x01 - Brian.mkv',
        'BBR_S52': 'Freddie 20x10 - Brian.mkv',
        'BBRAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        'BBRAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        'BBRAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        'BBR_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        'BBR_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        'BBRAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger.mkv',
        'BBRAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger.mkv',
        'BBRAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger.mkv',
        'BBR_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger.mkv',
        'BBR_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger.mkv',
        '_RJAS41': 'Freddie 02x001.mkv',
        '_RJAS52': 'Freddie 20x010.mkv',
        '_RJAS43': 'Freddie 02x100.mkv',
        '_RJ_S41': 'Freddie 02x01.mkv',
        '_RJ_S52': 'Freddie 20x10.mkv',
        '_RJAD41': 'Freddie 02x001 & 02x002 - Roger.mkv',
        '_RJAD52': 'Freddie 20x010 & 20x011 - Roger.mkv',
        '_RJAD43': 'Freddie 02x100 & 02x101 - Roger.mkv',
        '_RJ_D41': 'Freddie 02x01 & 02x02 - Roger.mkv',
        '_RJ_D52': 'Freddie 20x10 & 20x11 - Roger.mkv',
        '_RJAT41': 'Freddie 02x001 & 02x002 & 02x003 - Roger & John.mkv',
        '_RJAT52': 'Freddie 20x010 & 20x011 & 20x012 - Roger & John.mkv',
        '_RJAT43': 'Freddie 02x100 & 02x101 & 02x102 - Roger & John.mkv',
        '_RJ_T41': 'Freddie 02x01 & 02x02 & 02x03 - Roger & John.mkv',
        '_RJ_T52': 'Freddie 20x10 & 20x11 & 20x12 - Roger & John.mkv',
        '_R_AS41': 'Freddie 02x001.mkv',
        '_R_AS52': 'Freddie 20x010.mkv',
        '_R_AS43': 'Freddie 02x100.mkv',
        '_R__S41': 'Freddie 02x01.mkv',
        '_R__S52': 'Freddie 20x10.mkv',
        '_R_AD41': 'Freddie 02x001 & 02x002 - Roger.mkv',
        '_R_AD52': 'Freddie 20x010 & 20x011 - Roger.mkv',
        '_R_AD43': 'Freddie 02x100 & 02x101 - Roger.mkv',
        '_R__D41': 'Freddie 02x01 & 02x02 - Roger.mkv',
        '_R__D52': 'Freddie 20x10 & 20x11 - Roger.mkv',
        '_R_AT41': 'Freddie 02x001 & 02x002 & 02x003 - Roger.mkv',
        '_R_AT52': 'Freddie 20x010 & 20x011 & 20x012 - Roger.mkv',
        '_R_AT43': 'Freddie 02x100 & 02x101 & 02x102 - Roger.mkv',
        '_R__T41': 'Freddie 02x01 & 02x02 & 02x03 - Roger.mkv',
        '_R__T52': 'Freddie 20x10 & 20x11 & 20x12 - Roger.mkv',
        '_RBAS41': 'Freddie 02x001.mkv',
        '_RBAS52': 'Freddie 20x010.mkv',
        '_RBAS43': 'Freddie 02x100.mkv',
        '_RB_S41': 'Freddie 02x01.mkv',
        '_RB_S52': 'Freddie 20x10.mkv',
        '_RBAD41': 'Freddie 02x001 & 02x002 - Roger.mkv',
        '_RBAD52': 'Freddie 20x010 & 20x011 - Roger.mkv',
        '_RBAD43': 'Freddie 02x100 & 02x101 - Roger.mkv',
        '_RB_D41': 'Freddie 02x01 & 02x02 - Roger.mkv',
        '_RB_D52': 'Freddie 20x10 & 20x11 - Roger.mkv',
        '_RBAT41': 'Freddie 02x001 & 02x002 & 02x003 - Roger & Brian.mkv',
        '_RBAT52': 'Freddie 20x010 & 20x011 & 20x012 - Roger & Brian.mkv',
        '_RBAT43': 'Freddie 02x100 & 02x101 & 02x102 - Roger & Brian.mkv',
        '_RB_T41': 'Freddie 02x01 & 02x02 & 02x03 - Roger & Brian.mkv',
        '_RB_T52': 'Freddie 20x10 & 20x11 & 20x12 - Roger & Brian.mkv',
        '_RRAS41': 'Freddie 02x001.mkv',
        '_RRAS52': 'Freddie 20x010.mkv',
        '_RRAS43': 'Freddie 02x100.mkv',
        '_RR_S41': 'Freddie 02x01.mkv',
        '_RR_S52': 'Freddie 20x10.mkv',
        '_RRAD41': 'Freddie 02x001 & 02x002 - Roger.mkv',
        '_RRAD52': 'Freddie 20x010 & 20x011 - Roger.mkv',
        '_RRAD43': 'Freddie 02x100 & 02x101 - Roger.mkv',
        '_RR_D41': 'Freddie 02x01 & 02x02 - Roger.mkv',
        '_RR_D52': 'Freddie 20x10 & 20x11 - Roger.mkv',
        '_RRAT41': 'Freddie 02x001 & 02x002 & 02x003 - Roger.mkv',
        '_RRAT52': 'Freddie 20x010 & 20x011 & 20x012 - Roger.mkv',
        '_RRAT43': 'Freddie 02x100 & 02x101 & 02x102 - Roger.mkv',
        '_RR_T41': 'Freddie 02x01 & 02x02 & 02x03 - Roger.mkv',
        '_RR_T52': 'Freddie 20x10 & 20x11 & 20x12 - Roger.mkv',
        '__JAS41': 'Freddie 02x001.mkv',
        '__JAS52': 'Freddie 20x010.mkv',
        '__JAS43': 'Freddie 02x100.mkv',
        '__J_S41': 'Freddie 02x01.mkv',
        '__J_S52': 'Freddie 20x10.mkv',
        '__JAD41': 'Freddie 02x001 & 02x002.mkv',
        '__JAD52': 'Freddie 20x010 & 20x011.mkv',
        '__JAD43': 'Freddie 02x100 & 02x101.mkv',
        '__J_D41': 'Freddie 02x01 & 02x02.mkv',
        '__J_D52': 'Freddie 20x10 & 20x11.mkv',
        '__JAT41': 'Freddie 02x001 & 02x002 & 02x003 - John.mkv',
        '__JAT52': 'Freddie 20x010 & 20x011 & 20x012 - John.mkv',
        '__JAT43': 'Freddie 02x100 & 02x101 & 02x102 - John.mkv',
        '__J_T41': 'Freddie 02x01 & 02x02 & 02x03 - John.mkv',
        '__J_T52': 'Freddie 20x10 & 20x11 & 20x12 - John.mkv',
        '___AS41': 'Freddie 02x001.mkv',
        '___AS52': 'Freddie 20x010.mkv',
        '___AS43': 'Freddie 02x100.mkv',
        '____S41': 'Freddie 02x01.mkv',
        '____S52': 'Freddie 20x10.mkv',
        '___AD41': 'Freddie 02x001 & 02x002.mkv',
        '___AD52': 'Freddie 20x010 & 20x011.mkv',
        '___AD43': 'Freddie 02x100 & 02x101.mkv',
        '____D41': 'Freddie 02x01 & 02x02.mkv',
        '____D52': 'Freddie 20x10 & 20x11.mkv',
        '___AT41': 'Freddie 02x001 & 02x002 & 02x003.mkv',
        '___AT52': 'Freddie 20x010 & 20x011 & 20x012.mkv',
        '___AT43': 'Freddie 02x100 & 02x101 & 02x102.mkv',
        '____T41': 'Freddie 02x01 & 02x02 & 02x03.mkv',
        '____T52': 'Freddie 20x10 & 20x11 & 20x12.mkv',
        '__BAS41': 'Freddie 02x001.mkv',
        '__BAS52': 'Freddie 20x010.mkv',
        '__BAS43': 'Freddie 02x100.mkv',
        '__B_S41': 'Freddie 02x01.mkv',
        '__B_S52': 'Freddie 20x10.mkv',
        '__BAD41': 'Freddie 02x001 & 02x002.mkv',
        '__BAD52': 'Freddie 20x010 & 20x011.mkv',
        '__BAD43': 'Freddie 02x100 & 02x101.mkv',
        '__B_D41': 'Freddie 02x01 & 02x02.mkv',
        '__B_D52': 'Freddie 20x10 & 20x11.mkv',
        '__BAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        '__BAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        '__BAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        '__B_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        '__B_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        '__RAS41': 'Freddie 02x001.mkv',
        '__RAS52': 'Freddie 20x010.mkv',
        '__RAS43': 'Freddie 02x100.mkv',
        '__R_S41': 'Freddie 02x01.mkv',
        '__R_S52': 'Freddie 20x10.mkv',
        '__RAD41': 'Freddie 02x001 & 02x002.mkv',
        '__RAD52': 'Freddie 20x010 & 20x011.mkv',
        '__RAD43': 'Freddie 02x100 & 02x101.mkv',
        '__R_D41': 'Freddie 02x01 & 02x02.mkv',
        '__R_D52': 'Freddie 20x10 & 20x11.mkv',
        '__RAT41': 'Freddie 02x001 & 02x002 & 02x003 - Roger.mkv',
        '__RAT52': 'Freddie 20x010 & 20x011 & 20x012 - Roger.mkv',
        '__RAT43': 'Freddie 02x100 & 02x101 & 02x102 - Roger.mkv',
        '__R_T41': 'Freddie 02x01 & 02x02 & 02x03 - Roger.mkv',
        '__R_T52': 'Freddie 20x10 & 20x11 & 20x12 - Roger.mkv',
        '_BJAS41': 'Freddie 02x001.mkv',
        '_BJAS52': 'Freddie 20x010.mkv',
        '_BJAS43': 'Freddie 02x100.mkv',
        '_BJ_S41': 'Freddie 02x01.mkv',
        '_BJ_S52': 'Freddie 20x10.mkv',
        '_BJAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        '_BJAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        '_BJAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        '_BJ_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        '_BJ_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        '_BJAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & John.mkv',
        '_BJAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & John.mkv',
        '_BJAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & John.mkv',
        '_BJ_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & John.mkv',
        '_BJ_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & John.mkv',
        '_B_AS41': 'Freddie 02x001.mkv',
        '_B_AS52': 'Freddie 20x010.mkv',
        '_B_AS43': 'Freddie 02x100.mkv',
        '_B__S41': 'Freddie 02x01.mkv',
        '_B__S52': 'Freddie 20x10.mkv',
        '_B_AD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        '_B_AD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        '_B_AD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        '_B__D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        '_B__D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        '_B_AT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        '_B_AT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        '_B_AT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        '_B__T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        '_B__T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        '_BBAS41': 'Freddie 02x001.mkv',
        '_BBAS52': 'Freddie 20x010.mkv',
        '_BBAS43': 'Freddie 02x100.mkv',
        '_BB_S41': 'Freddie 02x01.mkv',
        '_BB_S52': 'Freddie 20x10.mkv',
        '_BBAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        '_BBAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        '_BBAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        '_BB_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        '_BB_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        '_BBAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian.mkv',
        '_BBAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian.mkv',
        '_BBAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian.mkv',
        '_BB_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian.mkv',
        '_BB_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian.mkv',
        '_BRAS41': 'Freddie 02x001.mkv',
        '_BRAS52': 'Freddie 20x010.mkv',
        '_BRAS43': 'Freddie 02x100.mkv',
        '_BR_S41': 'Freddie 02x01.mkv',
        '_BR_S52': 'Freddie 20x10.mkv',
        '_BRAD41': 'Freddie 02x001 & 02x002 - Brian.mkv',
        '_BRAD52': 'Freddie 20x010 & 20x011 - Brian.mkv',
        '_BRAD43': 'Freddie 02x100 & 02x101 - Brian.mkv',
        '_BR_D41': 'Freddie 02x01 & 02x02 - Brian.mkv',
        '_BR_D52': 'Freddie 20x10 & 20x11 - Brian.mkv',
        '_BRAT41': 'Freddie 02x001 & 02x002 & 02x003 - Brian & Roger.mkv',
        '_BRAT52': 'Freddie 20x010 & 20x011 & 20x012 - Brian & Roger.mkv',
        '_BRAT43': 'Freddie 02x100 & 02x101 & 02x102 - Brian & Roger.mkv',
        '_BR_T41': 'Freddie 02x01 & 02x02 & 02x03 - Brian & Roger.mkv',
        '_BR_T52': 'Freddie 20x10 & 20x11 & 20x12 - Brian & Roger.mkv',
    }


def get_batch_files_truth():
    return {
        "regex": [
            {
                "e_end": "6",
                "e_start": "4",
                "key": 0,
                "matches": [],
                "regex": "S[0-9]{2}E[0-9]{2}",
                "s_end": "3",
                "s_start": "1",
                "sxe": []
            },
            {
                "e_end": "6",
                "e_start": "4",
                "key": 1,
                "matches": [],
                "regex": "s[0-9]{2}e[0-9]{2}",
                "s_end": "3",
                "s_start": "1",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 2,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 3,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 4,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 5,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 6,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 7,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 8,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 9,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            }
        ],
        "units": [
            {
                "files": [],
                "select": False,
                "text": "04x04.mkv"
            },
            {
                "files": [],
                "select": False,
                "text": "0505.avi"
            },
            {
                "files": [
                    "01x01.mkv",
                    "s02e02.mkv",
                    "s02e02.srt",
                    "s03e03.srt"
                ],
                "opened": False,
                "select": False,
                "text": "season 01"
            }
        ]
    }


def get_batch_match_conf():
    return {
        "regex": [
            {
                "e_end": 6,
                "e_start": 4,
                "key": 0,
                "matches": [],
                "regex": "S[0-9]{2}E[0-9]{2}",
                "s_end": 3,
                "s_start": 1,
                "sxe": []
            },
            {
                "e_end": 6,
                "e_start": 4,
                "key": 1,
                "matches": [
                    "s02e02",
                    "s02e02",
                    "s03e03"
                ],
                "regex": "s[0-9]{2}e[0-9]{2}",
                "s_end": 3,
                "s_start": 1,
                "sxe": [
                    "02",
                    "02",
                    "02",
                    "02",
                    "03",
                    "03"
                ]
            },
            {
                "e_end": 5,
                "e_start": 3,
                "key": 2,
                "matches": [
                    "04x04",
                    "01x01"
                ],
                "regex": "[0-9]{2}x[0-9]{2}",
                "s_end": 2,
                "s_start": 0,
                "sxe": [
                    "04",
                    "04",
                    "01",
                    "01"
                ]
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 3,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 4,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 5,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 6,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 7,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 8,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            },
            {
                "e_end": "",
                "e_start": "",
                "key": 9,
                "matches": [],
                "regex": "",
                "s_end": "",
                "s_start": "",
                "sxe": []
            }
        ],
        "units": [
            {
                "files": [],
                "select": True,
                "text": "04x04.mkv"
            },
            {
                "files": [],
                "select": False,
                "text": "0505.avi"
            },
            {
                "files": [
                    "01x01.mkv",
                    "s02e02.mkv",
                    "s02e02.srt",
                    "s03e03.srt"
                ],
                "opened": False,
                "select": True,
                "text": "season 01"
            }
        ]
    }


def get_batch_match_truth():
    return {
        "anime": False,
        "files": [
            {
                "e_nr": 4,
                "episode_option": "Single",
                "location": "04x04.mkv",
                "s_nr": 4,
                "sub": False,
                "title": "",
                "title2": "",
                "title3": ""
            },
            {
                "e_nr": 1,
                "episode_option": "Single",
                "location": "season 01\\01x01.mkv",
                "s_nr": 1,
                "sub": False,
                "title": "",
                "title2": "",
                "title3": ""
            },
            {
                "e_nr": 2,
                "episode_option": "Single",
                "location": "season 01\\s02e02.mkv",
                "s_nr": 2,
                "sub": False,
                "title": "",
                "title2": "",
                "title3": ""
            },
            {
                "e_nr": 2,
                "episode_option": "Single",
                "location": "season 01\\subs\\s02e02.srt",
                "s_nr": 2,
                "sub": True,
                "title": "",
                "title2": "",
                "title3": ""
            },
            {
                "e_nr": 3,
                "episode_option": "Single",
                "location": "season 01\\subs\\s03e03.srt",
                "s_nr": 3,
                "sub": True,
                "title": "",
                "title2": "",
                "title3": ""
            }
        ],
        "final": "",
        "name_needed": True,
        "premiere": "",
        "series_name": "",
        "status": "",
        "tvdb_id": ""
    }


def get_batch_sync_conf():
    return {
    "anime": False,
    "files": [
        {
            "e_nr": 4,
            "episode_option": "Triple",
            "location": "04x04.mkv",
            "s_nr": 4,
            "sub": False,
            "sync": True,
            "title": "Kick the Ballistics",
            "title2": "Eye of the Beholder",
            "title3": "Demons"
        },
        {
            "e_nr": 1,
            "episode_option": "Single",
            "location": "season 01\\01x01.mkv",
            "s_nr": 1,
            "sub": False,
            "sync": True,
            "title": "",
            "title2": "Nanny McDead",
            "title3": "Hedge Fund Homeboys"
        },
        {
            "e_nr": 2,
            "episode_option": "Double",
            "location": "season 01\\s02e02.mkv",
            "s_nr": 2,
            "sub": False,
            "sync": True,
            "title": "The Double Down",
            "title2": "Inventing the Girl",
            "title3": "Fool Me Once..."
        },
        {
            "e_nr": 2,
            "episode_option": "Single",
            "location": "season 01\\subs\\s02e02.srt",
            "s_nr": 2,
            "sub": True,
            "sync": True,
            "title": "The Double Down",
            "title2": "Inventing the Girl",
            "title3": "Fool Me Once..."
        }
    ],
    "final": "",
    "name_needed": True,
    "premiere": "2009-03-09",
    "series_name": "Castle",
    "status": "Ended",
    "tvdb_id": 83462
}


def get_batch_sync_truth():
    return {
    "error": [
        "Copy failed: T:\\Subs\\Castle 02x02 - The Double Down.srt",
    ],
    "info": [
        "Series Name: Castle",
        "Status: Ended",
        "Season 4 created",
        "Season 1 created",
        "Season 2 created"
    ],
    "success": [
        "Copy successful: L:\\Series\\Castle\\Season 04\\Castle 04x04 & 04x05 & 04x06 - Kick the Ballistics & Eye of the Beholder & Demons.mkv",
        "Copy successful: L:\\Series\\Castle\\Season 01\\Castle 01x01.mkv",
        "Copy successful: L:\\Series\\Castle\\Season 02\\Castle 02x02 & 02x03 - The Double Down & Inventing the Girl.mkv"
    ],
    "summary": {
        "seasons": {
            "1": "Season 1: 1 Files (1 Episodes) copied",
            "2": "Season 2: 1 Files (2 Episodes) copied",
            "4": "Season 4: 1 Files (3 Episodes) copied"
        },
        "total": "3 Files (6 Episodes) copied"
    }
}


def get_error_truth():
    return [{'message': "LowerCase Error: d'Etat", 'old_location': '', 'title': "Blues & D'etat Part I", 'series_name': 'Tiny Dancer', 'e_nr': 1, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 1, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': "d'Etat", 'exception': False}, {'message': 'LowerCase Error: a', 'old_location': '', 'title': 'A Hand Above', 'series_name': 'Tiny Dancer', 'e_nr': 2, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 2, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': 'a', 'exception': False}, {'message': 'LowerCase Error: another', 'old_location': '', 'title': 'Grace Another Table & Raise Our Glasses Part IIIII', 'series_name': 'Tiny Dancer', 'e_nr': 3, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 3, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Double', 'anime': False, 'word': 'another', 'exception': False}, {'message': 'UpperCase Error: The', 'old_location': '', 'title': 'Raise the Glasses Part 9', 'series_name': 'Tiny Dancer', 'e_nr': 4, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 4, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': 'The', 'exception': False}, None, {'message': 'Unnecessary Part Number', 'old_location': '', 'title': "Blues & d'Etat Part I", 'series_name': 'Tiny Dancer', 'e_nr': 1, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 1, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, {'message': 'Part Number Roman Error', 'old_location': '', 'title': 'Grace another Table & Raise Our Glasses Part V', 'series_name': 'Tiny Dancer', 'e_nr': 3, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 3, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Double', 'anime': False, 'word': '', 'exception': False}, {'message': 'Part Number Integer Error', 'old_location': '', 'title': 'Raise The Glasses Part IX', 'series_name': 'Tiny Dancer', 'e_nr': 4, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 4, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, {'message': 'Unnecessary Part Numbers', 'old_location': '', 'title': 'Programmed to Receive Part I and Part I', 'series_name': 'Tiny Dancer', 'e_nr': 5, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 5, 'save': False, 'delete': False, 'extension': '', 'header': '', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Double', 'anime': False, 'word': '', 'exception': False}, None, None, None, {'message': 'Double Space', 'old_location': '', 'title': 'Tiny Dancer - Programmed to Receive Part II', 'series_name': 'Tiny Dancer', 'e_nr': 999, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 999, 'save': False, 'delete': False, 'extension': '', 'header': 'Tiny Dancer 01x - Programmed to  Receive Part II', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, {'message': 'Space Before Extension', 'old_location': '', 'title': 'Dancing @ the Sand', 'series_name': 'Tiny Dancer', 'e_nr': 8, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 8, 'save': False, 'delete': False, 'extension': '', 'header': 'Tiny Dancer 01x08 - Dancing in the Sand .mkv', 'tvdb_id': '', 'name_needed': False, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, None, None, {'message': 'Title Missing', 'old_location': '', 'title': '', 'series_name': 'Tiny Dancer', 'e_nr': 9, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 9, 'save': False, 'delete': False, 'extension': '', 'header': 'Tiny Dancer 02x08 - Dancing in the Sand .mkv', 'tvdb_id': '', 'name_needed': True, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, None, {'message': 'Symbol Error', 'old_location': '', 'title': 'Dancing @ the Sand ', 'series_name': 'Tiny Dancer', 'e_nr': 8, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 8, 'save': False, 'delete': False, 'extension': '', 'header': 'Tiny Dancer 01x08 - Dancing in the Sand .mkv', 'tvdb_id': '', 'name_needed': True, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, {'message': 'Episode Number Error', 'old_location': '', 'title': 'Tiny Dancer - Programmed to  Receive Part II', 'series_name': 'Tiny Dancer', 'e_nr': '', 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 999, 'save': False, 'delete': False, 'extension': '', 'header': 'Tiny Dancer 01x - Programmed to  Receive Part II', 'tvdb_id': '', 'name_needed': True, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, None, {'message': 'Season Number Error', 'old_location': '', 'title': '', 'series_name': 'Tiny Dancer', 'e_nr': 9, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 9, 'save': False, 'delete': False, 'extension': '', 'header': 'Tiny Dancer 02x08 - Dancing in the Sand .mkv', 'tvdb_id': '', 'name_needed': True, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}, {'message': 'Series Name Error', 'old_location': '', 'title': '', 'series_name': 'Tiny Dancer', 'e_nr': 10, 's_nr': 1, 's_nr_old': 1, 'e_nr_old': 10, 'save': False, 'delete': False, 'extension': '', 'header': 'Sensation 01x10 - In the Year.mkv', 'tvdb_id': '', 'name_needed': True, 'episode_option': 'Single', 'anime': False, 'word': '', 'exception': False}]

