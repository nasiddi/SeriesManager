import os

SERIES_DIR_TREE = 'L:\\Series'
SERIES_DIR = 'V:\\Series'
ANIME_DIR_TREE = 'L:\\Anime'
ANIME_DIR = 'V:\\Anime'
HD_Movies_TREE = 'L:\\HD'
HD_Movies = 'V:\\HD'
SD_MOVIES_TREE = 'L:\\SD'
SD_MOVIES = 'V:\\SD'


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

