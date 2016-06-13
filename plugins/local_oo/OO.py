# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, Qt

from .UI import OUi, MusicDatabaseTable, SongsTable
from libs.MySql_implement.LocalMusic import MysqlMusic


class OO(QObject):
    def __init__(self, app):
        super().__init__(parent=app)
        self._app = app

        self.ui = OUi(self._app)
        self.user = None

        self.bind_signal()

    def bind_signal(self):
        self.ui.login_btn.clicked.connect(self.ready_login)
        self.ui.login_dialog.login_btn.clicked.connect(self.login_check)
        self.ui.login_dialog.register_btn.clicked.connect(self.register)

        self.ui.songs_table_container.table_control.search_box.textChanged\
            .connect(self.search_table)
        self.ui.songs_table_container.table_control.search_box.returnPressed\
            .connect(self.search_net)

        self._app.player.signal_player_media_changed.connect(
            self.on_player_media_changed)

        self._app.ui.central_panel.left_panel.playlist_panel.playlist_signal.connect(
            self.show_playlist)

        self.ui.music_database_item.clicked.connect(self.show_database_songs)

        self.ui.songs_table_container.table_control.play_all_btn.clicked.connect(self.show_dialog)

    def ready_login(self):
        # show dialog
        self.ui.login_dialog.show()

    def login_check(self):
        username = str(self.ui.login_dialog.username_input.text())
        password = str(self.ui.login_dialog.password_input.text())
        mysql = MysqlMusic()
        state, uid = mysql.check_user_login(username, password)
        if state:
            self.ui.login_btn.setFixedSize(100, 30)
            self.ui.login_btn.setText('欢迎！' + username)
            self._app.set_uid(uid)
            self.ui.login_dialog.username_input.clear()
            self.ui.login_dialog.password_input.clear()
            self.ui.login_dialog.hide()
        else:
            pass  # jump a dialog show wrong message

    def register(self):
        username = str(self.ui.login_dialog.username_input.text())
        password = str(self.ui.login_dialog.password_input.text())
        mysql = MysqlMusic()
        uid = mysql.create_user_account(username, password)  # register and login
        if uid:
            self._app.set_uid(uid)
            self.ui.login_dialog.username_input.clear()
            self.ui.login_dialog.password_input.clear()
            self.ui.login_dialog.hide()
        else:
            pass  # jump a dialog show wrong message

    def search_table(self, text):
        songs_table = self.ui.songs_table_container.songs_table
        songs_table.search(text)

    def search_net(self):
        text = self.ui.songs_table_container.table_control.search_box.text()
        # connect to net and search, wait to do

    def on_player_media_changed(self, song):
        # In order to locate song position
        songs_table = self.ui.songs_table_container.songs_table
        songs_table.scroll_to_song(song)

    # def on_player_state_changed(self, state):
    #     if (state == QMediaPlayer.PlayingState
    #             or state == QMediaPlayer.PausedState):

    def play_song(self, song):
        self._app.player.play(song)

    def add_song_to_buy(self, song):
        if self._app.uid > 1:
            mysql = MysqlMusic()
            if not mysql.check_user_music_exist(self._app.uid, song.mid):
                mysql.insert_buy_log_to_user_music(self._app.uid, song.mid)
                mysql.update_music_all_buy_num(song.mid)
            else:
                self._app.message("你已经购买过了哦！", error=True)
        elif self._app.uid != 1:
            self._app.message("你还未登录，不能购买哟！", error=True)
        else:
            self._app.message("管理员同学你不用购买音乐！", error=True)

    def add_song_to_love(self, song):
        if self._app.uid > 0:
            mysql = MysqlMusic()
            if not mysql.check_user_love_exist(self._app.uid, song.mid):
                mysql.insert_love_log_to_user_music(self._app.uid, song.mid)
            else:
                self._app.message("你已经收藏过了哦!", error=True)
        else:
            self._app.message("你还未登录，不能收藏哟！", error=True)

    def load_songs(self, song_object=None):
        # Notice!
        # song table has set_songs
        # playlist dialog has set_songs
        load = MysqlMusic()
        if song_object is None:
            song_object = SongsTable()
        song_object.set_songs(load.get_all_music_from_sql())  # MysqlMusic ClassMethod

    def show_database_songs(self):
        db_songs_table = MusicDatabaseTable(self._app)
        self.load_songs(db_songs_table)  # load song to music database table

        db_songs_table.play_song_signal.connect(self.play_song)
        db_songs_table.buy_song_signal.connect(self.add_song_to_buy)
        db_songs_table.add_song_signal.connect(self._app.player.add_music)
        db_songs_table.love_song_signal.connect(self.add_song_to_love)
        # db_songs_table.set_to_next_signal.connect(
        #     self._app.player.set_tmp_fixed_next_song)   # it have some bug... wait to fix

        self.ui.songs_table_container.set_table(db_songs_table)  # set with search box table
        self._app.ui.central_panel.right_panel.set_widget(
            self.ui.songs_table_container)

    def save_playlist_to_sql(self):
        playlist_name = str(self.ui.playlist_dialog.playlist_name.text())
        mysql = MysqlMusic()
        if playlist_name:
            flag = True
            for box in self.ui.playlist_dialog.checkbox_list:
                if box.checkState() == Qt.Checked:
                    if flag:
                        pid = mysql.insert_item_into_w_playlist(playlist_name, self._app.uid)
                        flag = False
                    mysql.insert_playlist_to_playlist(pid, playlist_name, self._app.uid, box.song.mid)
                    box.setChecked(False)
            if flag:
                pass  # message False
            self.ui.playlist_dialog.close()
            self.ui.playlist_dialog.playlist_name.clear()
        else:
            pass  # message False

    def show_dialog(self):
        if self._app.uid > 1:
            self.ui.playlist_dialog.show()
            self.load_local(self.ui.playlist_dialog)
            self.ui.playlist_dialog.confirm_btn.clicked.connect(self.save_playlist_to_sql)
            # we get it from sql write to user
        elif self._app.uid == 1:
            self._app.message('管理员同学，你不需要歌单～', error=True)
        else:
            self._app.message("你还未登录哦~", error=True)

    def load_playlist(self, pid, p_name):
        mysql = MysqlMusic()
        songs = mysql.get_playlist_all_music(pid, p_name)
        return songs

    def show_playlist(self, playlist):
        pid = int(playlist[0])
        p_name = playlist[2]
        playlist_song_table = SongsTable(self._app)
        playlist_song_table.set_songs(self.load_playlist(pid, p_name))

        playlist_song_table.play_song_signal.connect(self.play_song)
        playlist_song_table.play_all_playlist_signal.connect(self.play_all)
        # playlist_song_table.add_song_signal.connect(self._app.player.add_music)
        # playlist_song_table.love_song_signal.connect(self.add_song_to_love)

        self.ui.songs_table_container.set_table(playlist_song_table)
        self._app.ui.central_panel.right_panel.set_widget(
            self.ui.songs_table_container)

    def play_all(self, songs):
        if songs is not None:
            self._app.player.set_music_list(songs)

    def net_searcher(self):
        text = self.ui.songs_table_container.table_control.search_box.text()