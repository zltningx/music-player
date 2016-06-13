# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer

from setting import DEFAULT_FILE_PATH, APP_ICON
from theme import ThemeManager
from MusicBox_UI import Ui, MyMusicTable
from libs.widgets.base import MFrame
from libs.widgets.components import MusicTable
from player import Player
from player_mode import PlayerModeManager
from utils import darker
from libs.MySql_implement.LocalMusic import MysqlMusic


class App(MFrame):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager(self)
        self.player = Player(self)
        self.player_mode_manager = PlayerModeManager(self)

        self.theme_manager.set_theme(DEFAULT_FILE_PATH)

        self.ui = Ui(self)
        self._uid = 0  # 0 is none user 1 is admin and other were user

        self.resize(960, 600)
        self.setObjectName('app')
        self.set_theme_style()
        self.bind_signal()
        self.get_all_playlist()

        self.player_img = None  # Icon and background img from mp3

    def bind_signal(self):
        top_panel = self.ui.top_panel
        status_panel = self.ui.status_panel
        library_panel = self.ui.central_panel.left_panel.library_panel

        self.player.stateChanged.connect(self._on_player_status_changed)
        self.player.positionChanged.connect(self._on_player_position_changed)
        self.player.durationChanged.connect(self._on_player_duration_changed)
        self.player.signal_player_media_changed.connect(
            self._on_player_song_changed)
        self.player.signal_playback_mode_changed.connect(
            status_panel.pms_btn.on_playback_mode_changed)

        status_panel.pms_btn.clicked.connect(self.player.next_playback_mode)
        status_panel.theme_switch_btn.signal_change_theme.connect(
            self.theme_manager.choose_theme)
        status_panel.theme_switch_btn.clicked.connect(self.refresh_themes)

        top_panel.pc_panel.volume_slider.sliderMoved.connect(
            self.change_volume)
        top_panel.pc_panel.play_btn.clicked.connect(self.player.play_or_pause)
        top_panel.pc_panel.next_btn.clicked.connect(self.player.play_next)
        top_panel.pc_panel.previous_btn.clicked.connect(self.player.play_last)

        library_panel.current_playlist_item.clicked.connect(
            self.show_current_playlist)
        library_panel.music_buy_item.clicked.connect(self.show_buy_music)
        library_panel.music_love_item.clicked.connect(self.show_love_music)
        library_panel.music_rank.clicked.connect(self.show_rank_list)

        self.ui.current_playlist_table.play_song_signal.connect(
                self.player.play)
        self.ui.current_playlist_table.remove_signal.connect(
                self.player.remove_music)

    def _on_player_status_changed(self, status):
        play_btn = self.ui.top_panel.pc_panel.play_btn
        if status == QMediaPlayer.PlayingState:
            play_btn.setText('暂停')
        else:
            play_btn.setText('播放')

    def _on_player_song_changed(self, song):
        song_label = self.ui.status_panel.song_label
        song_label.set_song(song.title + ' - ' + song.artists)
        self.player_img = self.set_background(song.img)
        if self.player_img is not None:
            QApplication.setWindowIcon(QIcon(self.player_img))
        self.update()

    def _on_player_duration_changed(self, ms):
        self.ui.top_panel.pc_panel.progress_label.set_duration(ms)
        self.ui.top_panel.pc_panel.progress_slider.set_duration(ms)

    def _on_player_position_changed(self, ms):
        self.ui.top_panel.pc_panel.progress_slider.update_state(ms)
        self.ui.top_panel.pc_panel.progress_label.update_state(ms)

    def set_background(self, data):
        img = QImage()
        img.loadFromData(data)
        pixmap = QPixmap(img)
        if pixmap.isNull():
            return None
        return pixmap

    def paintEvent(self, event):
        # paint background
        painter = QPainter(self)
        bg_color = darker(self.theme_manager.current_theme.background, a=200)

        if self.player_img is not None:
            pixmap = self.player_img.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, pixmap)
            painter.fillRect(self.rect(), bg_color)

    def refresh_themes(self):
        theme_switch_btn = self.ui.status_panel.theme_switch_btn
        themes = self.theme_manager.list()
        theme_switch_btn.set_themes(themes)

    def show_current_playlist(self):
        # when clicked playlist
        self.ui.current_playlist_table.set_songs(self.player.songs)  # songs return music list
        right_panel = self.ui.central_panel.right_panel  # connected to music table
        right_panel.set_widget(self.ui.current_playlist_table)  # set widget to this table

    def show_buy_music(self):
        # when clicked buy item
        if self._uid < 1:
            self.message('你还没有登录哦', error=True)
            return
        elif self._uid == 1:
            self.message("管理员同学你不需要购买哦", error=True)
            return
        # TODO: SQL QUERY
        right_panel = self.ui.central_panel.right_panel  # the same as show_current_playlist
        mysql = MysqlMusic()
        songs = mysql.get_user_buy_music(self._uid)  # load song

        my_music = MyMusicTable(self)   # set Widget
        my_music.set_songs(songs)

        my_music.play_song_signal.connect(self.play_song)
        right_panel.set_widget(my_music)

    def show_love_music(self):
        # when clicked love item
        if self._uid < 1:
            self.message('你还没有登录哦', error=True)
            return

        # TODO: SQL QUERY
        right_panel = self.ui.central_panel.right_panel  # the same as show_current_playlist
        mysql = MysqlMusic()
        songs = mysql.get_user_love_music(self._uid)  # load song

        my_music = MyMusicTable(self)   # set Widget
        my_music.set_songs(songs)

        my_music.play_song_signal.connect(self.play_song)
        right_panel.set_widget(my_music)

    def show_rank_list(self):
        right_panel = self.ui.central_panel.right_panel
        mysql = MysqlMusic()
        songs = mysql.get_rank_list()

        rank_list = MyMusicTable(self)
        rank_list.set_songs(songs)

        rank_list.play_song_signal.connect(self.play_song)
        right_panel.set_widget(rank_list)

    def play_song(self, song):
        self.player.play(song)

    def change_volume(self, value):
        self.player.setVolume(value)

    def message(self, text, error=False):
        self.ui.status_panel.message.show_message(text, error)

    def set_theme_style(self):
        theme = self.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.background.name(),
                   theme.foreground.name())
        self.setStyleSheet(style_str)

    @property
    def uid(self):
        return self._uid

    def set_uid(self, uid):
        # login call
        self._uid = uid

    def get_all_playlist(self):
        mysql = MysqlMusic()
        playlist = mysql.get_all_playlist_from_sql()
        for name in playlist:
            self.ui.central_panel.left_panel.playlist_panel.\
                add_playlist(str(name[0]) + '  -  ' + name[1])  # item is playlist name. see localmusic.py

    def closeEvent(self, event):
        self.player.stop()
        QApplication.quit()