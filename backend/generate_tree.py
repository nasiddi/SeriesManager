import os
import platform


if platform.system() == 'Windows':
    SERIES_DIR_TREE = 'L:\\Series'
    SERIES_DIR = 'V:\\Series'
    ANIME_DIR_TREE = 'L:\\Anime'
    ANIME_DIR = 'V:\\Anime'
    HD_Movies_TREE = 'L:\\HD'
    HD_Movies = 'V:\\HD'
    SD_MOVIES_TREE = 'L:\\SD'
    SD_MOVIES = 'V:\\SD'
else:
    SERIES_DIR_TREE = '/Volumes/Downloads/Series'
    SERIES_DIR = '/Volumes/Video/Series'
    ANIME_DIR_TREE = '/Volumes/Downloads/Anime'
    ANIME_DIR = '/Volumes/Video/Anime'
    HD_Movies_TREE = '/Volumes/Downloads/HD'
    HD_Movies = '/Volumes/Video/HD'
    SD_MOVIES_TREE = '/Volumes/Downloads/SD'
    SD_MOVIES ='/Volumes/Video/SD'


def build_tree(src, des):
    print('creating Tree of ', src)
    for root, _, files in os.walk(src):
        if 'Specials' in root:
            continue
        des_root = root.replace(src, des)
        print(root)
        try:
            os.makedirs(des_root)
        except FileExistsError:
            pass
        for name in files:
            f = open(os.path.join(des_root, name), 'w+')
            f.close()


build_tree(ANIME_DIR, ANIME_DIR_TREE)
build_tree(SERIES_DIR, SERIES_DIR_TREE)
build_tree(HD_Movies, HD_Movies_TREE)
build_tree(SD_MOVIES, SD_MOVIES_TREE)

