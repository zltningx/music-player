# -*- coding: utf-8 -*-

import platform
import time
from functools import wraps
from PyQt5.QtGui import QColor


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        result = func(*args, **kwargs)
        elapsed_time = time.process_time() - t

        return result
    return wrapper


def parse_ms(ms):
    minute = int(ms / 60000)
    second = int((ms % 60000) / 1000)
    return minute, second


def get_ms(ms):
    minute = int(ms / 60)
    second = int((ms % 60))
    if len(str(minute)) < 2:
        minute = '0' + str(minute)
    if len(str(second)) < 2:
        second = '0' + str(second)
    return str(minute), str(second)


def lighter(color, degree=1, a=255):
    r, g, b = color.red(), color.green(), color.blue()
    r = r + 10 * degree if (r + 10 * degree) < 255 else 255
    g = g + 10 * degree if (g + 10 * degree) < 255 else 255
    b = b + 10 * degree if (b + 10 * degree) < 255 else 255
    return QColor(r, g, b, a)


def darker(color, degree=1, a=255):
    r, g, b = color.red(), color.green(), color.blue()
    r = r - 10 * degree if (r - 10 * degree) > 0 else 0
    g = g - 10 * degree if (g - 10 * degree) > 0 else 0
    b = b - 10 * degree if (b - 10 * degree) > 0 else 0
    return QColor(r, g, b, a)


def is_linux():
    if platform.system() == 'Linux':
        return True
    return False


def is_osx():
    if platform.system() == 'Darwin':
        return True
    return False

