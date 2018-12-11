import os
from utils.io_utlis import *
from utils.constants import *
import error_search
from os.path import join
from series import Series
from episode import Episode


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



def test_error_search():
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



def get_episodes():
    episodes = []


def create_error_search_tree():
    tree = [FILE_DIR, ['Series', ['Tiny Dancer',
                                  ['Season 01',
                                   'Tiny Dancer 01x01 - The A.mkv',
                                   'Tiny Dancer 01x02 - The & a Part I',
                                   'Tiny Dancer 01x03 - the Voices Part II.txt']]]

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


test_error_search()
