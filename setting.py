# -*- coding: utf-8 -*-

import os
import asyncio
from enum import Enum

BASE_PATH = '/home/ling/musicbox/music_player'

DEFAULT_FILE_PATH = BASE_PATH + '/themes/Solarized.cs'
THEME_FILE_PATH = [
    BASE_PATH + '/themes/',
]

APP_ICON = BASE_PATH + '/static_file/'

SONG_DIR = BASE_PATH + '/static_file/music_file/'


class PlaybackMode(Enum):
    one_loop = '单曲循环'
    sequential = '顺序'  # other mode
    loop = '全部循环'
    random = '随机'