from utils.file import File
import unittest
from episode import Episode
from utils.constants import *
from utils.io_utlis import load_shows
from series import Series
import stats


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
                                #print(s)
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

    def test_stats(self):
        statistics = stats.main(['--output=stats.json'])
        self.assertTrue(statistics)



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
