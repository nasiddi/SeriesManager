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
SERIES_DIR = 'L:\\Series' if DEBUG else 'V:\\Series'
ANIME_DIR = 'L:\\Anime' if DEBUG else 'V:\\Anime'
TREE = 'C:\\Users\\nadina\\Documents\\code\\FileManager\\assets\\tree\\Series'
HD_Movies = 'L:\\HD' if DEBUG else 'V:\\HD'
SD_MOVIES = 'L:\\SD' if DEBUG else 'V:\\SD'
FILE_DIR = 'L:\\complete\\' if DEBUG else 'V:\\downloads\\'
META_FILE = 'metadata.json'
SUB_DIR = 'T:\\Subs'
LOCK_File = 'data\\shows.lock'
OUT_FILE = 'OUTPUT_FILE'

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



