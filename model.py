# -*- coding: utf-8 -*-

import datetime
from mutagen.mp3 import MP3
import os


class SongModel(object):
    def __init__(self, mid, url):
        self._mid = mid
        self._url = url
        self.mp3_suffix()  # get music title, artist etc.
        self._start_time = datetime.datetime.now()
        self._buy_num = 0

    def mp3_suffix(self):
        mp3Info = MP3(self._url)
        try:
            self._title = mp3Info['TIT2'].text[0]
        except:
            self._title = 'Unknown Title'
        try:
            self._length = mp3Info.info.length
        except:
            self._length = 0  # can't read music
        try:
            self._artists = mp3Info['TPE1'].text[0]
        except:
            self._artists = 'Unknown Artists'
        try:
            self._album = mp3Info['TALB'].text[0]
        except:
            self._album = "Unknown Album"
        try:
            self._img = mp3Info['APIC:'].data
        except:
            try:
                self._img = mp3Info['APIC:e'].data
            except:
                self._img = b''

    @property
    def mid(self):
        return self._mid

    @property
    def title(self):
        return self._title

    @property
    def artists(self):
        return self._artists

    @property
    def album(self):
        return self._album

    @property
    def length(self):
        return float(self._length)

    @property
    def url(self):
        return self._url

    @property
    def img(self):
        return self._img

    @property
    def buy_num(self):
        return self._buy_num


class PlaylistModel(object):
    def __init__(self, pid, name, uid, songs=[]):
        super().__init__()
        self._pid = pid
        self._name = name
        self._uid = uid
        self._songs = songs

    def get_songs_from_sql(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def songs(self):
        if self.songs:
            return self._songs

    @classmethod
    def add_songs(cls, mid):
        # wait to do
        pass

    @classmethod
    def del_songs(cls, mid):
        # wait to do
        pass