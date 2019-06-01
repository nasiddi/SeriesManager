import platform

DEBUG = True if platform.system() == 'Windows' else False

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

ASSETS = 'assets'
LOCK_File = 'assets/shows.lock'
OUT_FILE = 'OUTPUT_FILE'
CONF_FILE = 'CONF_FILE'
META_FILE = 'assets/metadata.json'
DICT_FILE = 'assets/dictionary.json'
SHOWS_FILE = 'assets/shows.pkl'
BACKUP_DIR = 'assets/backup'
EXCEPTIONS_FILE = 'assets/exceptions.json'

if platform.system() == 'Windows':
    SERIES_DIR = 'L:\\Series' if DEBUG else 'V:\\Series'
    ANIME_DIR = 'L:\\Anime' if DEBUG else 'V:\\Anime'
    HD_Movies = 'L:\\HD' if DEBUG else 'V:\\HD'
    SD_MOVIES = 'L:\\SD' if DEBUG else 'V:\\SD'
    FILE_DIR = 'L:\\complete\\' if DEBUG else 'V:\\downloads\\'
    SUB_DIR = 'T:\\Subs'
    LOG_DIR = 'T:\\watch'
    LOCAL_DIR = 'C:\\Users\\Nadina\\Downloads\\complete'
    
    MAC_OFFSET = 0

else:
    SERIES_DIR = '/Volumes/Downloads/Series' if DEBUG else '/Volumes/Video/Series'
    ANIME_DIR = '/Volumes/Downloads/Anime' if DEBUG else '/Volumes/Video/Anime'
    HD_Movies = '/Volumes/Downloads/HD' if DEBUG else '/Volumes/Video/HD'
    SD_MOVIES = '/Volumes/Downloads/SD' if DEBUG else '/Volumes/Video/SD'
    FILE_DIR = '/Volumes/Downloads/complete/' if DEBUG else '/Volumes/Video/downloads/'
    SUB_DIR = '/Volumes/Temp/Subs'
    LOG_DIR = '/Volumes/Temp/watch'
    LOCAL_DIR = '/Users/nadina/Downloads'

    MAC_OFFSET = 2

# Extensions
EXTENSIONS = ['mp4', 'mkv', 'avi', 'flv', 'm4v', 'divx', 'webm', 'mpg']
SUBS = ['idx', 'sub', 'srt']


# Meta Fields
STATUS = 'status'
NAME_NEEDED = 'name_needed'
PREMIERE = 'premiere'
FINAL = 'final'
TVDB_ID = 'tvdb_id'
SERIES_NAME = 'series_name'
LOCATION = 'location'


# Pattern
ANIME_PATTERN = '\s[0-9]{2}x[0-9]{3}[.\s]'
SERIES_PATTERN = '\s[0-9]{2}x[0-9]{2}[.\s]'
ASPECT_RATIOS = {1.25: '5:4', 1.33333: '4:3', 1.5: '3:2', 1.77777: '16:9'}
QUALITY = {360: 'SD', 720: 'HD', 1080: 'FullHD', 2160: '4K'}

WRONG_SYMBOLS = [
      ':',
      '/',
      '{',
      '}',
      '\\',
      '<',
      '>',
      '*',
      '?',
      '$',
      '!',
      '@',
    ]

NUMERALS = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

# print('meta', os.path.exists(META_FILE))
# print('series', os.path.exists(SERIES_DIR))
# print('anime', os.path.exists(ANIME_DIR))
# print('hd', os.path.exists(HD_Movies))
# print('sd', os.path.exists(SD_MOVIES))
# print('file', os.path.exists(FILE_DIR))
# print('subs', os.path.exists(SUB_DIR))
