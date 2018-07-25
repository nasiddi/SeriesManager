# Status
NONE = 'none'
AIRING = 'airing'
HIATUS = 'hiatus'
ENDED = 'ended'


def get_status(status):
    if status == AIRING:
        return AIRING
    elif status == HIATUS:
        return HIATUS
    elif status == ENDED:
        return ENDED
    else:
        return NONE


# Locations
SERIES_DIR = 'V:\\Series'
ANIME_DIR = 'V:\\Anime'
TREE = 'C:\\Users\\nadina\\Documents\\code\\FileManager\\assets\\tree\\Series'
HD_Movies = 'L:\\complete\\HD'
SD_MOVIES = 'L:\\complete\\SD'
FILE_DIR = 'L:\\complete'
META_FILE = 'meta.json'

# Extentions

EXTENTIONS = ['mp4', 'mkv', 'avi', 'flv', 'm4v', 'divx', 'webm']
SUBS = ['idx', 'sub', 'srt']


# Meta Fields
STATUS = 'Status'
NAME_NEEDED = 'Name Needed'
PREMIERE = 'Premiere'
FINAL = 'Final'
EP_NAMES = 'Names'

# Pattern
ANIME_PATTERN = '[0-9]{2}x[0-9]{3}'
SERIES_PATTERN = '[0-9]{2}x[0-9]{2}'



