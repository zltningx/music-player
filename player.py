# -*- coding: utf-8 -*-

import asyncio
import random

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QTimer

from setting import PlaybackMode
from utils import parse_ms
from model import SongModel


class Player(QMediaPlayer):
    signal_player_media_changed = pyqtSignal([SongModel])  # media button clicked
    signal_playlist_is_empty = pyqtSignal()  # if playlist is empty
    signal_playback_mode_changed = pyqtSignal([PlaybackMode])  # media play mode changed
    signal_playlist_finished = pyqtSignal()  # playlist finished

    signal_song_required = pyqtSignal()  # ?
    finished = pyqtSignal()  # song finished

    _music_list = list()  # music_model object
    _current_index = None
    current_song = None
    _tmp_fix_next_song = None
    playback_mode = PlaybackMode.loop  # default mode
    last_playback_mode = PlaybackMode.loop  # last mode
    _other_mode = False

    def __init__(self, app):
        super().__init__(app)
        self._app = app
        self. _stalled_timer = QTimer(self)

        self.error.connect(self.on_error_occured)
        self.mediaChanged.connect(self.on_media_changed)
        self.mediaStatusChanged.connect(self.on_media_status_changed)
        self._stalled_timer.timeout.connect(self._wait_to_seek_back)

        self._music_error_times = 0
        self._retry_latency = 0
        self._music_error_maximum = 0

        self._media_stalled = False

    # These functions are about the playback mode
    def _record_playback_mode(self):
        # record current playback mode.
        self.last_playback_mode = self.playback_mode

    def _set_playback_mode(self, mode):
        """ set playback mode to :param mode
        item once: 0
        item in loop: 1
        sequential: 2
        loop: 3
        random: 4
        """
        if mode == self.playback_mode:
            return 0
        self._record_playback_mode()  # record play mode
        self.playback_mode = mode
        self._app.message('设置播放模式: {}'.format(mode.value))
        self.signal_playback_mode_changed.emit(mode)

    def change_player_mode_to_normal(self):
        # implement for player mode manager
        self._other_mode = False
        self._set_playback_mode(self.last_playback_mode)

    def change_player_mode_to_other(self):
        # implement for player mode manager
        self._other_mode = True
        self._set_playback_mode(PlaybackMode.sequential)

    def next_playback_mode(self):
        if self.playback_mode == PlaybackMode.one_loop:
            self._set_playback_mode(PlaybackMode.loop)
        elif self.playback_mode == PlaybackMode.loop:
            self._set_playback_mode(PlaybackMode.random)
        elif self.playback_mode == PlaybackMode.random:
            self._set_playback_mode(PlaybackMode.one_loop)

    # in these functions are about QMedia Play control
    @pyqtSlot(QMediaContent)
    def on_media_changed(self, media_content):
        music_model = self._music_list[self._current_index]
        self.signal_player_media_changed.emit(music_model)

    @pyqtSlot(QMediaPlayer.MediaStatus)
    def on_media_status_changed(self, state):
        self._media_stalled = False
        if state == QMediaPlayer.EndOfMedia:  # finished and turn to next
            self.finished.emit()
            self.stop()
            if (self._current_index == len(self._music_list) - 1) and\
                    self._other_mode:
                self.signal_playlist_finished.emit()
            if not self._other_mode:
                self.play_next()
        elif state in (QMediaPlayer.BufferedMedia, QMediaPlayer.LoadedMedia):
            self.play()
        elif state in (QMediaPlayer.StalledMedia,):
            self.pause()
            self._media_stalled = True
            if not self._stalled_timer.isActive():
                self._stalled_timer.start()
                self._stalled_timer.setInterval(3000)

    def is_music_in_list(self, model):
        for music in self._music_list:
            if model.mid == music.mid:  # Focus this line of code music model's mid 未定
                return True
        return False

    def insert_to_next(self, model):
        # if not in music list return False
        # else insert next to current music of music list
        if not self.is_music_in_list(model):
            if self._current_index is None:
                index = 0
            else:
                index = self._current_index + 1
            self._music_list.insert(index, model)
            return True
        return False

    def add_music(self, model):
        self._music_list.append(model)

    def remove_music(self, mid):
        for i, music_model in enumerate(self._music_list):
            if mid == music_model.mid:
                self._music_list.pop(i)  # i is the index of removed music
                if self._current_index is not None:
                    if i == self._current_index:
                        self.play_next()
                    elif i < self._current_index:
                        self._current_index -= 1  # if current index bigger than i
                    return True
        return False

    def set_music_list(self, music_list):
        """ implement of music list
        the most import implement of Player class.
        in this function we will setting current music list via music_list.
        :param music_list:  a list object with music object.
        """
        # initialization private member '_music_list', clear current music list.
        self._music_list = list()
        self._music_list = music_list
        if len(self._music_list):
            self.play(self._music_list[0])

    def clear_playlist(self):
        # initialization private member '_music_list', clear current music list.
        self._music_list = list()
        self._current_index = None
        self.current_song = None
        self.stop()

    def get_media_content_from_model(self, music_model):
        url = music_model.url
        if not url:
            self._app.message("Music Doesn't exist ！ 歌曲不存在")
            return None
        if url.startswith('http:'):  # implement of any web music site api
            media_content = QMediaContent(QUrl(url))
        else:
            media_content = QMediaContent(QUrl.fromLocalFile(url))  # attribute 'absoluteFilePath' of QFileInfo object
        return media_content

    def _play(self, music_model):
        """ real play model
        :param music_model: music model ready to play
        :return: True or False
        """
        insert_flag = self.insert_to_next(music_model)
        index = self.get_index_by_model(music_model)
        if not insert_flag and self._current_index is not None:  # if music_model is current music
            if music_model.mid == self.current_song.mid\
                    and self.state() == QMediaPlayer.PlayingState:  # if current state is Playing state
                return True
        super().stop()
        media_content = self.get_media_content_from_model(music_model)  # get music_model media content
        if media_content is not None:
            self._app.message("load music: {}...".format(music_model.title))
            self._current_index = index
            self.current_song = music_model
            self.setMedia(media_content)
            return True
        else:
            self._app.message("{} cannot play, turn to next".format(music_model.title))
            self.remove_music(music_model.mid)  # delete from music list
            self.play_next()
            return False

    def other_mode_play(self, music_model):
        self._play(music_model)

    def play(self, music_model=None):
        """ rewrite QMediaPlayer.play()
        :param music_model: playing song while music_model is None
        """
        if music_model is None:
            super().play()
            return False
        self._app.message("Playing: {}".format(music_model.title))
        self._app.player_mode_manager.exit_to_normal()
        self._play(music_model)

    def play_or_pause(self):
        if len(self._music_list) is 0:
            self.signal_playlist_is_empty.emit()
            return
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        elif self.state() == QMediaPlayer.PausedState:
            self.play()
        else:
            self.play_next()

    def set_tmp_fixed_next_song(self, song):
        self._tmp_fix_next_song = song

    def play_next(self):
        """ play next song
        :return: if not empty play next music and return True,
        else return False.
        """
        if self._tmp_fix_next_song is not None:
            flag = self.play(self._tmp_fix_next_song)
            self._tmp_fix_next_song = None
            return flag
        index = self.get_next_song_index()
        if index is not None:
            if index == 0 and self._other_mode:  #
                self.signal_playlist_finished.emit()
                return
            music_model = self._music_list[index]
            self.play(music_model)
            return True
        else:
            self.signal_playlist_is_empty.emit()
            return False

    def play_last(self):
        index = self.get_prior_song_index()
        if index is not None:
            music_model = self._music_list[index]
            self.play(music_model)

    def get_index_by_model(self, music_model):
        for i, music in enumerate(self._music_list):
            if music_model.mid == music.mid:
                return i
        return None

    def get_next_song_index(self):
        # next song
        # select song via playback_mode
        if len(self._music_list) is 0:
            return None
        if self.playback_mode == PlaybackMode.one_loop:
            return self._current_index
        elif self.playback_mode == PlaybackMode.loop:
            if self._current_index >= len(self._music_list) - 1:
                return 0
            else:
                return self._current_index + 1
        elif self.playback_mode == PlaybackMode.sequential:
            self.signal_playlist_finished.emit()
            return None
        else:
            return random.choice(range(len(self._music_list)))

    def get_prior_song_index(self):
        # previous song
        # select song via playback_mode
        if len(self._music_list) is 0:
            return None
        if self.playback_mode == PlaybackMode.one_loop:
            return self._current_index
        elif self.playback_mode == PlaybackMode.loop:
            if self._current_index is 0:
                return len(self._music_list) - 1
            else:
                return self._current_index - 1
        elif self.playback_mode == PlaybackMode.sequential:
            return None
        else:
            return random.choice(range(len(self._music_list)))

    # Error detail
    @pyqtSlot(QMediaPlayer.Error)
    def on_error_occured(self, error):
        song = self._music_list[self._current_index]
        self._app.message("{} cannot play".format(song.title))
        self.stop()
        if error == QMediaPlayer.FormatError:
            self._app.message("Format Error", error=True)
        else:
            self._wait_to_next(2)  #
            self._app.message("Turn to next one", error=True)

    def _wait_to_next(self, second=0):
        if len(self._music_list) < 2:  # only one in or less in music list
            return
        app_event_loop = asyncio.get_event_loop()
        app_event_loop.call_later(second, self.play_next)  # function as an argument

    def _wait_to_seek_back(self):
        if not self._media_stalled:
            return
        self._app.message("seek back")
        self._media_stalled = False
        self._stalled_timer.stop()
        current_position = self.position()
        two_second_back = current_position - 1 * 1000
        if two_second_back < 0:
            two_second_back = 0
        self.setPosition(two_second_back)

    @property
    def songs(self):
        return self._music_list