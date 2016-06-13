# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRect
from PyQt5.QtWidgets import (QMenu, QAction, QHeaderView, QVBoxLayout,
                             QAbstractItemView, QHBoxLayout, QMainWindow,
                             QWidget, QCheckBox)

from libs.widgets.base import (MLabel, MFrame, MQLineEdit, MButton,
                               MDialog, MScrollArea)
from libs.widgets.components import MusicTable, LPGroupItem
from model import SongModel


# usual playlist table
class SongsTable(MusicTable):
    play_song_signal = pyqtSignal([SongModel])
    add_song_signal = pyqtSignal([SongModel])
    play_all_playlist_signal = pyqtSignal([list])

    def __init__(self, app, rows=0, colums=6, parent=None):
        super().__init__(app, rows, colums, parent)
        self._app = app
        self.songs = list()

        self.setObjectName('playlist_table')
        self.set_theme_style()
        self.setHorizontalHeaderLabels(['', '音乐名', '歌手', '专辑', '时长',
                                        ''])
        self.setColumnWidth(0, 28)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(5, 100)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)

        self._context_menu_row = 0
        self._drag_row = None

    @pyqtSlot()
    def add_song_to_current_playlist(self):
        # do not call explicit, this just a slot function
        song = self.songs[self._context_menu_row]
        self.add_song_signal.emit(song)  # SongModel

    @pyqtSlot()
    def play_all_playlist(self):
        self.play_all_playlist_signal.emit(self.songs)

    def contextMenuEvent(self, event):
        menu = QMenu()
        add_to_current_playlist_action = QAction('加入播放队列', self)
        play_all_playlist_action = QAction("播放歌单", self)
        menu.addAction(add_to_current_playlist_action)
        menu.addAction(play_all_playlist_action)
        add_to_current_playlist_action.triggered.connect(
            self.add_song_to_current_playlist)
        play_all_playlist_action.triggered.connect(self.play_all_playlist)
        # remove_song_from_playlist_action.triggered.connect(
        #     self.remove_song_from_playlist)

        point = event.pos()
        item = self.itemAt(point)
        if item is not None:
            row = self.row(item)
            self._context_menu_row = row
            menu.exec(event.globalPos())

    def scroll_to_song(self, song):
        # locate song position
        for i, s in enumerate(self.songs):
            if s.mid == song.mid:
                item = self.item(i, 1)
                self.scrollToItem(item)
                self.setCurrentItem(item)
                break

    @property
    def drag_song(self):
        if self._drag_row is not None:
            return self.songs[self._drag_row]
        return None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        point = event.pos()
        item = self.itemAt(point)
        if item is not None:
            self._drag_row = self.row(item)

    def on_cell_db_click(self, row, column):
        song = self.songs[row]
        self.play_song_signal.emit(song)


class MusicDatabaseTable(MusicTable):
    play_song_signal = pyqtSignal([SongModel])
    buy_song_signal = pyqtSignal([SongModel])
    love_song_signal = pyqtSignal([SongModel])
    set_to_next_signal = pyqtSignal([SongModel])
    add_song_signal = pyqtSignal([SongModel])

    def __init__(self, app, rows=0, columns=6, parent=None):
        super().__init__(app, rows, columns, parent)
        self._app = app
        self.songs = list()

        self.setObjectName('database_songs_table')
        self.set_theme_style()
        self.setHorizontalHeaderLabels(['', '音乐名', '歌手', '专辑', '时长',
                                        ''])
        self.setColumnWidth(0, 28)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(5, 100)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)

        self._context_menu_row = 0
        self._drag_row = None

    @pyqtSlot()
    def add_song_to_current_playlist(self):
        # do not call explicit, this just a slot function
        song = self.songs[self._context_menu_row]
        self.add_song_signal.emit(song)

    @pyqtSlot()
    def add_song_to_love(self):
        # do not call explicit, this just a slot function
        song = self.songs[self._context_menu_row]
        self.love_song_signal.emit(song)

    @pyqtSlot()
    def set_song_to_next(self):
        # do not call explicit, this just a slot function
        song = self.songs[self._context_menu_row]
        self.set_to_next_signal.emit(song)

    @pyqtSlot()
    def add_song_to_buy(self):
        # do not call explicit, this just a slot function
        song = self.songs[self._context_menu_row]
        self.buy_song_signal.emit(song)

    # @pyqtSlot()
    # def remove_song_from_playlist(self):
    #     # do not call explicit, this just a slot function
    #     song = self.songs[self._context_menu_row]

    def contextMenuEvent(self, event):
        menu = QMenu()
        add_to_current_playlist_action = QAction('加入播放队列', self)
        add_to_buy_music = QAction('购买歌曲', self)
        add_to_love_music = QAction("收藏歌曲", self)
        menu.addAction(add_to_current_playlist_action)
        menu.addAction(add_to_buy_music)
        menu.addAction(add_to_love_music)

        add_to_current_playlist_action.triggered.connect(
            self.add_song_to_current_playlist)
        add_to_buy_music.triggered.connect(self.add_song_to_buy)
        add_to_love_music.triggered.connect(self.add_song_to_love)

        point = event.pos()
        item = self.itemAt(point)
        if item is not None:
            row = self.row(item)
            self._context_menu_row = row
            menu.exec(event.globalPos())

    def scroll_to_song(self, song):
        # locate song position
        for i, s in enumerate(self.songs):
            if s.mid == song.mid:
                item = self.item(i, 1)
                self.scrollToItem(item)
                self.setCurrentItem(item)
                break

    @property
    def drag_song(self):
        if self._drag_row is not None:
            return self.songs[self._drag_row]
        return None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        point = event.pos()
        item = self.itemAt(point)
        if item is not None:
            self._drag_row = self.row(item)

    def on_cell_db_click(self, row, column):
        song = self.songs[row]
        self.play_song_signal.emit(song)


class SearchBox(MQLineEdit):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.setObjectName('search_box')
        self.setPlaceholderText('搜索歌曲、歌手')
        self.setToolTip('输入文字可以从当前歌单内搜索\n'
                        '按下 Enter 将搜索网络')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                padding-left: 3px;
                font-size: 14px;
                background: transparent;
                border: 0px;
                border-bottom: 1px solid {1};
                color: {2};
                outline: none;
            }}
            #{0}:focus {{
                outline: none;
            }}
        '''.format(self.objectName(),
                   theme.color6.name(),
                   theme.foreground.name())
        self.setStyleSheet(style_str)


class TableControl(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.play_all_btn = MButton('创建歌单')
        self.search_box = SearchBox(self._app)
        self._layout = QHBoxLayout(self)
        self.setup_ui()
        self.setObjectName('n_table_control')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            QPushButton {{
                background: transparent;
                color: {1};
                font-size: 16px;
                outline: none;
            }}
            QPushButton:hover {{
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color0.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setFixedHeight(40)
        self.play_all_btn.setFixedSize(80, 20)
        self.search_box.setFixedSize(160, 26)

        self._layout.addSpacing(20)
        self._layout.addWidget(self.play_all_btn)
        self._layout.addStretch(0)
        self._layout.addWidget(self.search_box)
        self._layout.addSpacing(60)


class SongsTableContainer(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.songs_table = None
        self.table_control = TableControl(self._app)
        self._layout = QVBoxLayout(self)
        self.setup_ui()

    def set_table(self, songs_table):
        if self.songs_table:
            self._layout.replaceWidget(self.songs_table, songs_table)
            self.songs_table.deleteLater()
        else:
            self._layout.addWidget(songs_table)
            self._layout.addSpacing(10)
        self.songs_table = songs_table

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.table_control)


class LineInput(MQLineEdit):
    def __int__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.setObjectName('line_input')
        self.set_theme_style()

    def set_theme_style(self):
        pass


class LoginDialog(MDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.username_input = LineInput(self)
        self.password_input = LineInput(self)
        self.password_input.setEchoMode(MQLineEdit.Password)
        self.login_btn = MButton('登录', self)
        self.register_btn = MButton('注册', self)
        self._login_frame = MFrame()
        self._login_layout = QHBoxLayout(self._login_frame)
        self._layout = QVBoxLayout(self)

        self.username_input.setPlaceholderText('用户名或管理员backdoor登录')
        self.password_input.setPlaceholderText('密码')

        self.setObjectName('login_dialog')
        self.set_theme_style()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(200)

        self._login_layout.setContentsMargins(0, 0, 0, 0)
        self._login_layout.setSpacing(1)
        self._login_layout.addWidget(self.login_btn)
        self._login_layout.addWidget(self.register_btn)

        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.username_input)
        self._layout.addWidget(self.password_input)
        self._layout.addWidget(self._login_frame)


class LoginButton(MLabel):
    clicked = pyqtSignal()

    def __init__(self, app, text=None, parent=None):
        super().__init__(text, parent)
        self._app = app

        self.setText('登录')
        self.setToolTip('用户或管理员登录')
        self.setObjectName('oo_login_btn')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                color: {1};
            }}
            #{0}:hover {{
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color4.name())
        self.setStyleSheet(style_str)

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton and
                self.rect().contains(event.pos())):
            self.clicked.emit()


class MyCheckBox(MFrame):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        # self.header = MLabel("请选择歌曲并确认", self._app)
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self.set_theme_style()
        self.setObjectName("my_checkbox")
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
            }}
        '''.format(self.objectName(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # self._layout.addWidget(self.header)
        self._layout.addStretch(1)

    def add_item(self, checkbox):
        self._layout.addWidget(checkbox)


class PlaylistCenterPanelContainer(MScrollArea):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self.check_group = MyCheckBox(self._app)

        self.setObjectName('pc_container')
        self._layout = QVBoxLayout(self)
        self.setWidget(self.check_group)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
            }}
        '''.format(self.objectName(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)


class DialogButton(MButton):
    def __init__(self, app, text=None, parent=None):
        super().__init__(text, parent)
        self._app = app
        self.setObjectName('d_button')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                font-size: 13px;
                color: {1};
            }}
            #{0}:hover {{
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.color0.name(),
                   theme.color4.name())
        self.setStyleSheet(style_str)


class PlaylistName(MQLineEdit):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self.setObjectName('playlist_name')
        self.setPlaceholderText('请输入歌单名称,并选择歌曲保存')

        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                padding-left: 3px;
                font-size: 14px;
                background: {3};
                border: 0px;
                border-bottom: 1px solid {1};
                color: {2};
                outline: none;
            }}
            #{0}:focus {{
                outline: none;
            }}
        '''.format(self.objectName(),
                   theme.color6.name(),
                   theme.foreground.name(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)


class OCheckBox(QCheckBox):
    def __init__(self, app, text=None, song=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("my_check_box")
        self._app = app
        self._song = song

        self.set_theme_style()

    @property
    def song(self):
        return self._song

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {3};
                font-size: 13px;
                color: {1};
                outline: none;
            }}
            #{0}:hover {{
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color4.name(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)


class PlaylistDialog(MDialog):
    # checkbox_checked_signal = pyqtSignal([SongModel])

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self.setObjectName("playlist_dialog")
        self.check_container = PlaylistCenterPanelContainer(self._app, self)
        self.playlist_name = PlaylistName(self._app, self)
        self.confirm_cancel_group = MFrame(self._app)
        self.confirm_cancel_layout = QHBoxLayout(self.confirm_cancel_group)
        self.confirm_btn = DialogButton(self._app, '确认', self)
        self.cancel_btn = DialogButton(self._app, '取消', self)
        self._layout = QVBoxLayout(self)
        self._checkbox = list()

        self.set_theme_style()

        self.setup_ui()

    @property
    def checkbox_list(self):
        return self._checkbox

    def setup_ui(self):
        self.setFixedWidth(500)
        self.setFixedHeight(600)
        self.confirm_cancel_layout.setContentsMargins(0, 0, 0, 0)
        self.confirm_cancel_layout.setSpacing(0)
        self.confirm_cancel_layout.addWidget(self.confirm_btn)
        self.confirm_cancel_layout.addWidget(self.cancel_btn)

        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.playlist_name)
        self._layout.addWidget(self.check_container)
        self._layout.addWidget(self.confirm_cancel_group)

    def set_songs(self, songs):
        for song in songs:
            self.add_checkbox(song)

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
            }}
        '''.format(self.objectName(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def add_checkbox(self, song):
        song_str = song.title + '   --   ' + song.artists + '   --   ' + song.album
        song_checkbox = OCheckBox(self._app, song_str, song, self)
        self._checkbox.append(song_checkbox)
        self.check_container.check_group.add_item(song_checkbox)


class OUi(object):
    def __init__(self, app):
        self._app = app
        self.songs_table_container = SongsTableContainer(self._app)
        self._lb_container = MFrame()
        self.login_dialog = LoginDialog(self._app, self._app)
        self.playlist_dialog = PlaylistDialog(self._app, self._app)
        self.login_btn = LoginButton(self._app)

        self.music_database_item = LPGroupItem(self._app, '音乐库')
        self.music_database_item.set_img_text('Ω')

        self._lbc_layout = QHBoxLayout(self._lb_container)
        self.setup()

    def setup(self):
        self._lbc_layout.setContentsMargins(0, 0, 0, 0)
        self._lbc_layout.setSpacing(0)

        self._lbc_layout.addWidget(self.login_btn)
        self.login_btn.setFixedSize(30, 30)
        self._lbc_layout.addSpacing(10)

        # TODO: connect with Main APP
        tp_layout = self._app.ui.top_panel.layout()
        tp_layout.addWidget(self._lb_container)
        library_panel = self._app.ui.central_panel.left_panel.library_panel
        library_panel.add_item(self.music_database_item)  # action in OO.py