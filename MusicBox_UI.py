# -*- coding: utf-8 -*-

import asyncio
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import Qt, QTime, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMenu, QAction
from PyQt5.QtMultimedia import QMediaPlayer

from libs.widgets.base import (MButton, MFrame, MLabel, MScrollArea,
                                MComboBox)
from libs.widgets.sliders import _BasicSlider
from libs.widgets.labels import _BasicLabel
from libs.widgets.components import LPGroupHeader, LPGroupItem, MusicTable
from setting import PlaybackMode
from utils import parse_ms
from model import SongModel


# PlayerControlButton, ProgressSlider, ProgressLabel and VolumeSlider,
# this four class used by PlayerControlPanel Class.
# MusicPlayer Frame were formed by those Class.
class PlayerControlButton(MButton):
    def __init__(self, app, text=None, parent=None):
        super().__init__(text, parent)
        self._app = app

        self.setObjectName('mc_btn')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                font-size: 13px;
                color: {1};
                outline: none;
            }}
            #{0}:hover {{
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color4.name())
        self.setStyleSheet(style_str)


class ProgressSlider(_BasicSlider):
    def __init__(self, app, parent=None):
        super().__init__(app, parent)

        self.setOrientation(Qt.Horizontal)
        self.setMinimumWidth(400)
        self.setObjectName('player_progress_slider')

        self.sliderMoved.connect(self.seek)

    def set_duration(self, ms):
        self.setRange(0, ms / 1000)  # Range 0-ms/1000

    def update_state(self, ms):
        self.setValue(ms / 1000)  # setting value of progress slider

    def seek(self, second):
        self._app.player.setPosition(second * 1000)  # locate position of progress


class ProgressLabel(_BasicLabel):
    def __init__(self, app, text=None, parent=None):
        super().__init__(app, text, parent)
        self._app = app

        self.duration_text = '00:00'

        self.setObjectName('player_progress_label')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName(),
                    theme.color3.name())
        self.setStyleSheet(self._style_str + style_str)

    def set_duration(self, ms):
        """set duration text
        :param ms: time mm:ss
        """
        m, s = parse_ms(ms)  # deal minute and second to QTime arguments
        duration = QTime(0, m, s)
        print(m,s)
        self.duration_text = duration.toString('mm:ss')

    def update_state(self, ms):
        """update current state in progress Label
        :param ms: time mm:ss
        """
        m, s = parse_ms(ms)
        position = QTime(0, m, s)
        position_text = position.toString('mm:ss')
        self.setText(position_text + '/' + self.duration_text)


class VolumeSlider(_BasicSlider):
    def __init__(self, app, parent=None):
        super().__init__(app, parent)

        self.setOrientation(Qt.Horizontal)
        self.setMinimumWidth(100)
        self.setObjectName('player_volume_slider')
        self.setRange(0, 100)
        self.setValue(100)
        self.setToolTip('调节音量')


class PlayerControlPanel(MFrame):
    """PlayerControl Framework
    consist: player control button, music progress, volume progress.
    """
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)
        self.previous_btn = PlayerControlButton(self._app, '上一首', self)  # pointed btn parent to self
        self.play_btn = PlayerControlButton(self._app, '播放', self)
        self.next_btn = PlayerControlButton(self._app, '下一首', self)
        self.progress_slider = ProgressSlider(self._app, self)
        self.volume_slider = VolumeSlider(self._app, self)
        self.progress_label = ProgressLabel(self._app, '00:00/00:00', self)

        self._btn_container = MFrame(self)
        self._slider_container = MFrame(self)

        self._bc_layout = QHBoxLayout(self._btn_container)
        self._sc_layout = QHBoxLayout(self._slider_container)

        self.setObjectName('pc_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                color: {1};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color0.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._btn_container.setFixedWidth(140)
        self._slider_container.setMinimumWidth(700)
        self.progress_label.setFixedWidth(90)

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._bc_layout.setSpacing(0)
        self._bc_layout.setContentsMargins(0, 0, 0, 0)

        self._bc_layout.addWidget(self.previous_btn)
        self._bc_layout.addStretch(1)
        self._bc_layout.addWidget(self.play_btn)
        self._bc_layout.addStretch(1)
        self._bc_layout.addWidget(self.next_btn)

        self._sc_layout.addWidget(self.progress_slider)
        self._sc_layout.addSpacing(2)
        self._sc_layout.addWidget(self.progress_label)
        self._sc_layout.addSpacing(5)
        self._sc_layout.addStretch(0)
        self._sc_layout.addWidget(self.volume_slider)
        self._sc_layout.addStretch(1)

        self._layout.addWidget(self._btn_container)
        self._layout.addSpacing(10)
        self._layout.addWidget(self._slider_container)


class SongOperationPanel(MFrame):
    """SongOperationPanel
    """
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self.setObjectName('song_operation_panel')
        self.set_theme_style()

    def set_theme_style(self):
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName())
        self.setStyleSheet(style_str)


class TopPanel(MFrame):
    """TopPanel consist with SongOperationPanel, PlayerControlPanel
    """
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)
        self.pc_panel = PlayerControlPanel(self._app, self)
        self.mo_panel = SongOperationPanel(self._app, self)

        self.setObjectName('top_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                color: {1};
                border-bottom: 3px inset {3};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color0_light.name(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setFixedHeight(50)
        self._layout.addSpacing(5)
        self._layout.addWidget(self.pc_panel)
        self._layout.addWidget(self.mo_panel)


# TODO: This area about CenterPanel, consist with left panel and right panel
class LPLibraryPanel(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.header = LPGroupHeader(self._app, '我的音乐')
        self.current_playlist_item = LPGroupItem(self._app, '当前播放列表')
        self.current_playlist_item.set_img_text('❂')
        self.music_buy_item = LPGroupItem(self._app, '壕买的音乐')
        self.music_buy_item.set_img_text('♫')
        self.music_love_item = LPGroupItem(self._app, '买不起的音乐')
        self.music_love_item.set_img_text('♡')
        self.music_rank = LPGroupItem(self._app, '排行榜')
        self.music_rank.set_img_text('☢')
        self._layout = QVBoxLayout(self)

        self.setObjectName('lp_library_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName(),
                   theme.color3.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addSpacing(3)
        self._layout.addWidget(self.header)
        self._layout.addWidget(self.current_playlist_item)
        self._layout.addWidget(self.music_buy_item)
        self._layout.addWidget(self.music_love_item)
        self._layout.addWidget(self.music_rank)

    def add_item(self, item):
        self._layout.addWidget(item)

    def add_playlist(self, name):
        # implement: add playlist to buy current playlist
        item = LPGroupItem(self._app, name)
        self.add_item(item)


class LPPlaylistPanel(MFrame):
    playlist_signal = pyqtSignal([list])

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.header = LPGroupHeader(self._app, '歌单')
        self._layout = QVBoxLayout(self)
        self.setObjectName('lp_playlist_panel')

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName(),
                   theme.color5.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addWidget(self.header)

    def add_item(self, item):
        self._layout.addWidget(item)

    def get_playlist_songs(self):
        item = self.sender()
        self.playlist_signal.emit(item.name.split())

    def add_playlist(self, name):
        # implement: add playlist to create playlist
        item = LPGroupItem(self._app, name)
        item.clicked.connect(self.get_playlist_songs)
        self.add_item(item)


class LeftPanel(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.library_panel = LPLibraryPanel(self._app)
        self.playlist_panel = LPPlaylistPanel(self._app)

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)  # activate layout
        self.setObjectName('c_left_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName(),
                   theme.color5.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addWidget(self.library_panel)
        self._layout.addWidget(self.playlist_panel)
        self._layout.addStretch(1)


# Scroll Area Connected to Left Panel Widget
class LeftPanelContainer(MScrollArea):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.left_panel = LeftPanel(self._app)
        self._layout = QVBoxLayout(self)  # no layout, no children
        self.setWidget(self.left_panel)  # set Widget connect to self(self is ScrollArea)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)  # Widget can resize

        self.setObjectName('c_left_panel_container')
        self.set_theme_style()
        self.setMinimumWidth(180)
        self.setMaximumWidth(221)

        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                border: 0px;
                border-right: 3px inset {1};
            }}
        '''.format(self.objectName(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)


class RightPanel(MFrame):
    # RightPanel's widget is changeable
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.widget = None
        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)
        self.setObjectName('right_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

    def set_widget(self, widget):
        # set or change widget
        if self.widget and self.widget != widget:
            self._layout.removeWidget(self.widget)
            self.widget.hide()
            widget.show()
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget)
        self.widget = widget


# The same as Left
class RightPanelContainer(MScrollArea):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.right_panel = RightPanel(self._app)
        self._layout = QVBoxLayout(self)
        self.setWidget(self.right_panel)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setObjectName('c_right_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                border: 0px;
            }}
        '''.format(self.objectName(),
                   theme.color5.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)


# contain Left and Right panel
class CentralPanel(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.left_panel_container = LeftPanelContainer(self._app, self)
        self.right_panel_container = RightPanelContainer(self._app, self)
        self.left_panel = self.left_panel_container.left_panel
        self.right_panel = self.right_panel_container.right_panel

        self._layout = QHBoxLayout(self)
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addWidget(self.left_panel_container)
        self._layout.addWidget(self.right_panel_container)


# TODO: This area about status frame
class SongLabel(MLabel):
    def __init__(self, app, text=None, parent=None):
        super().__init__()
        self._app = app
        self.setObjectName('song_label')
        self.setIndent(5)
        self.set_theme_style()

        self.set_song('准备开始听歌吧 ！ 少年')

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.color7.name(),
                   theme.color0.name())
        self.setStyleSheet(style_str)

    def set_song(self, song_text):
        self.setText('♪  ' + song_text + ' ')


class PlaybackModeSwitchBtn(MButton):
    def __init__(self, app, parent=None):
        super().__init__(parent=parent)
        self._app = app

        self.setObjectName('player_mode_switch_btn')
        self.set_theme_style()
        self.setText('循环')

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
                border: 0px;
                padding: 0px 4px;
            }}
        '''.format(self.objectName(),
                   theme.color6.name(),
                   theme.background.name())
        self.setStyleSheet(style_str)

    def set_text(self, text):
        self.setText('♭ ' + text)

    def on_playback_mode_changed(self, playback_mode):
        # wait clicked event
        if playback_mode == PlaybackMode.sequential:
            self.setText(self._app.player.current_mode.name)
        else:
            self.setText(playback_mode.value)


# Theme Boxmy
class ThemeComboBox(MComboBox):
    clicked = pyqtSignal()  # rewrite clicked signal
    signal_change_theme = pyqtSignal([str])  # signal: theme name

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.setObjectName('theme_switch_btn')
        self.setEditable(False)
        self.maximum_width = 150
        self.set_theme_style()
        self.setFrame(False)
        self.current_theme = self._app.theme_manager.current_theme.name
        self.themes =[self.current_theme]
        self.set_themes(self.themes)

        self.currentIndexChanged.connect(self.on_index_changed)

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
                border: 0px;
                padding: 0px 4px;
                border-radius: 0px;
            }}
            #{0}::drop-down {{
                width: 0px;
                border: 0px;
            }}
            #{0} QAbstractItemView {{
                border: 0px;
                min-width: 200px;
            }}
        '''.format(self.objectName(),
                   theme.color4.name(),
                   theme.background.name(),
                   theme.foreground.name())
        self.setStyleSheet(style_str)

    @pyqtSlot(int)
    def on_index_changed(self, index):
        if index < 0 or not self.themes:
            return
        metrics = QFontMetrics(self.font())
        if self.themes[index] == self.current_theme:
            return
        self.current_theme = self.themes[index]
        name = '❀ ' + self.themes[index]
        width = metrics.width(name)
        if width < self.maximum_width:
            self.setFixedWidth(width + 10)
            self.setItemText(index, name)
            self.setToolTip(name)
        else:
            self.setFixedWidth(self.maximum_width)
            text = metrics.elidedText(name, Qt.ElideRight,
                                      self.width())
            self.setItemText(index, text)
            self.setToolTip(text)
        self.signal_change_theme.emit(self.current_theme)

    def add_item(self, text):
        self.addItem('❀ ' + text)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton and
                self.rect().contains(event.pos())):
            self.clicked.emit()
            self.showPopup()

    def set_themes(self, themes):
        self.clear()
        if self.current_theme:
            self.themes = [self.current_theme]
            self.add_item(self.current_theme)
        else:
            self.themes = []
        for theme in themes:
            if theme not in self.themes:
                self.add_item(theme)
                self.themes.append(theme)


class MessageLabel(MLabel):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.setObjectName('message_label')
        self._interval = 3
        self.queue = list()
        self.hide()

    @property
    def common_style(self):
        style_str = '''
            #{0} {{
                padding-left: 3px;
                padding-right: 5px;
            }}
        '''.format(self.objectName())
        return style_str

    def _set_error_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.color1_light.name(),
                   theme.color7_light.name())
        self.setStyleSheet(style_str + self.common_style)

    def _set_normal_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.color6_light.name(),
                   theme.color7.name())
        self.setStyleSheet(style_str + self.common_style)

    def show_message(self, text, error=False):
        if self.isVisible():
            self.queue.append({'error': error, 'message': text})
            self._interval = 1.5
            return
        if error:
            self._set_error_style()
        else:
            self._set_normal_style()
        self.setText(str(len(self.queue)) + ':' + text)
        self.show()
        app_event_loop = asyncio.get_event_loop()
        app_event_loop.call_later(self._interval, self.access_message_queue)

    def access_message_queue(self):
        if self.isVisible():
            self.hide()
        if self.queue:
            m = self.queue.pop(0)
            self.show_message(m['message'], m['error'])
        else:
            self._interval = 3


class StatusPanel(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)
        self.message_label = MessageLabel(self._app)
        self.song_label = SongLabel(self._app, parent=self)
        self.pms_btn = PlaybackModeSwitchBtn(self._app, self)
        self.theme_switch_btn = ThemeComboBox(self._app, self)
        self.message_label = MessageLabel(self._app)

        self.setup_ui()
        self.setObjectName('status_panel')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
            }}
        '''.format(self.objectName(),
                   theme.color0.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setFixedHeight(18)

        self.song_label.setMaximumWidth(300)
        self._layout.addWidget(self.message_label)
        self._layout.addStretch(0)
        self._layout.addWidget(self.theme_switch_btn)
        self._layout.addWidget(self.pms_btn)
        self._layout.addWidget(self.song_label)

    @property
    def message(self):
        return self.message_label


class CurrentPlaylistTable(MusicTable):
    remove_signal = pyqtSignal([int])

    def __init__(self, app):
        super().__init__(app)
        self._app = app

        self._row = 0

        self.menu = QMenu()
        self.remove = QAction('从当前列表移除', self)
        self.menu.addAction(self.remove)

        self.remove.triggered.connect(self.remove_song)

    def contextMenuEvent(self, event):
        point = event.pos()
        item = self.itemAt(point)
        if item is not None:
            row = self.row(item)
            self._row = row
            self.menu.exec(event.globalPos())

    def remove_song(self):
        song = self.songs[self._row]
        self.songs.pop(self._row)
        self.removeRow(self._row)
        self.remove_signal.emit(song.mid)  # emit mid please Look at player.py


class MyMusicTable(MusicTable):
    play_song_signal = pyqtSignal([SongModel])

    def __init__(self, app):
        super().__init__(app)
        self._app = app

        self._row = 0

    def contextMenuEvent(self, event):
        point = event.pos()
        item = self.itemAt(point)
        if item is not None:
            row = self.row(item)
            self._row = row
            self.menu.exec(event.globalPos())

    def on_cell_db_click(self, row, column):
        song = self.songs[row]
        self.play_song_signal.emit(song)


class Ui(object):
    def __init__(self, app):
        self._layout = QVBoxLayout(app)
        self.top_panel = TopPanel(app, app)
        self.central_panel = CentralPanel(app, app)
        self.status_panel = StatusPanel(app, app)
        self.current_playlist_table = CurrentPlaylistTable(app)

        self.set_up()

    def set_up(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.top_panel)
        self._layout.addWidget(self.central_panel)
        self._layout.addWidget(self.status_panel)