import platform
import os

DEBUG = True


# Status
NONE = 'none'
AIRING = 'Airing'
HIATUS = 'Hiatus'
ENDED = 'Ended'

# Episode Options
SINGLE = 'Single'
DOUBLE = 'Double'
TRIPLE = 'Triple'

# Locations

LOCK_File = 'data\\shows.lock'
OUT_FILE = 'OUTPUT_FILE'

if platform.system() == 'Windows':
    SERIES_DIR = 'L:\\Series' if DEBUG else 'V:\\Series'
    ANIME_DIR = 'L:\\Anime' if DEBUG else 'V:\\Anime'
    HD_Movies = 'L:\\HD' if DEBUG else 'V:\\HD'
    SD_MOVIES = 'L:\\SD' if DEBUG else 'V:\\SD'
    FILE_DIR = 'L:\\complete\\' if DEBUG else 'V:\\downloads\\'
    SUB_DIR = 'T:\\Subs'
    META_FILE = 'data\\metadata.json'

else:
    SERIES_DIR = '/Volumes/Downloads/Series' if DEBUG else '/Volumes/Video/downloads/Series'
    ANIME_DIR = '/Volumes/Downloads/Anime' if DEBUG else '/Volumes/Video/downloads/Anime'
    HD_Movies = '/Volumes/Downloads/HD' if DEBUG else '/Volumes/Video/downloads/HD'
    SD_MOVIES = '/Volumes/Downloads/SD' if DEBUG else '/Volumes/Video/downloads/SD'
    FILE_DIR = '/Volumes/Downloads/complete/' if DEBUG else '/Volumes/Video/downloads/'
    SUB_DIR = '/Volumes/Temp/Subs'
    META_FILE = 'data/metadata.json'


# Extentions

EXTENTIONS = ['mp4', 'mkv', 'avi', 'flv', 'm4v', 'divx', 'webm']
SUBS = ['idx', 'sub', 'srt']


# Meta Fields
STATUS = 'status'
NAME_NEEDED = 'name_needed'
PREMIERE = 'premiere'
FINAL = 'final'
TVDB_ID = 'tvdb_id'
SERIES_NAME = 'series_name'


# Pattern
ANIME_PATTERN = '[0-9]{2}x[0-9]{3}'
SERIES_PATTERN = '[0-9]{2}x[0-9]{2}'

wrongSymbols = [
      ':',
      '/',
      '{',
      '}',
      '(',
      ')',
      '\\',
      '<',
      '>',
      '*',
      '?',
      '$',
      '!',
      '@',
    ]

print('meta', os.path.exists(META_FILE))
print('series', os.path.exists(SERIES_DIR))
print('anime', os.path.exists(ANIME_DIR))
print('hd', os.path.exists(HD_Movies))
print('sd', os.path.exists(SD_MOVIES))
print('file', os.path.exists(FILE_DIR))
print('subs', os.path.exists(SUB_DIR))





