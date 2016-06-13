# -*- coding: utf-8 -*-

import os

from model import SongModel
from setting import SONG_DIR
from .MySql_Executor import MySql


class MysqlMusic(object):
    def __init__(self):
        self.mysql = MySql()
        self.song_urls = self.scan()
        self.song_model = list()

    def _init_sql(self):
        """ init music_all table
        WARNING ! NOTICE PLEASE!
        this function should be dangerous,
        you should use it carefully.
        DON'T CALL IT DIRECTLY!
        AHH.
        """
        if self.song_urls is not None:
            for i, url in enumerate(self.song_urls):
                try:
                    song = SongModel(i, url)
                    self.mysql.insert_into_music_all(i, song.title,
                                                     song.artists, url,
                                                     song.length, song.album,
                                                     song.buy_num)
                except Exception as e:
                    print(e)
        else:
            print('[-]ERROR: dir empty!')

    def scan(self, dir=SONG_DIR):
        """ scan song dir
        :param dir: defined in setting file
        :return: songs url list
        """
        song_urls = list()
        name = os.listdir(dir)
        for i in name:
            song_urls.append(dir+i)  # here should be fix if file is mp3
        return song_urls

    def get_all_music_from_sql(self):
        """get_all_music
        :return: song_model
        """
        songs = list()
        musics, num = self.mysql.select_mid_url_from_music_all()
        for i in range(num):
            song = SongModel(musics[i][0], musics[i][1])
            songs.append(song)
        return songs

    def get_rank_list(self):
        songs = list()
        musics = self.mysql.select_music_from_rank()
        for music in musics:
            song = SongModel(music[0], music[1])
            songs.append(song)
        return songs

    def get_all_rank_list_from_music_all(self):
        songs = list()
        musics = self.mysql.select_rank_from_music_all()
        # 这个就是获取music数据表中所有的rank的函数

    def get_all_playlist_from_sql(self):
        playlist = list()
        names, num = self.mysql.select_playlist_from_w_playlist()
        for i in range(num):
            tmp = list()
            tmp.append(names[i][0])
            tmp.append(names[i][1])
            playlist.append(tmp)
        return playlist

    def get_user_buy_music(self, uid):
        songs = list()
        musics, num = self.mysql.select_mid_from_user_music(uid)
        for i in range(num):
            url = self.mysql.select_url_from_music_all(musics[i][0])
            song = SongModel(musics[i][0], url[0][0])
            songs.append(song)
        return songs

    def get_user_love_music(self, uid):
        songs = list()
        musics, num = self.mysql.select_mid_from_user_love(uid)
        for i in range(num):
            url = self.mysql.select_url_from_music_all(musics[i][0])
            song = SongModel(musics[i][0], url[0][0])
            songs.append(song)
        return songs

    def get_playlist_all_music(self, pid, name):
        songs = list()
        mids, num = self.mysql.select_mid_from_playlist(pid, name)
        for i in range(num):
            url = self.mysql.select_url_from_music_all(mids[i][0])
            song = SongModel(mids[i][0], url[0][0])
            songs.append(song)
        return songs

    # def get_user_playlist(self, uid):
    #     my_playlist = list()
    #     playlist, num = self.mysql.select_all_from_w_playlist(uid)
    #     for i in range(num):
    #         if not playlist[i][2]:
    #             p_name = playlist[i][1]
    #             my_playlist.append(p_name)
    #     return my_playlist

    def create_user_account(self, username, password):
        if self.mysql.insert_into_c_user(username, password, 0):
            uid = self.mysql.select_uid_from_c_user(username)
            return uid[0][0]
        else:
            return False

    def check_user_login(self, username, password):
        pwd = self.mysql.select_password_from_c_user(username)
        uid = self.mysql.select_uid_from_c_user(username)
        if pwd:
            if pwd[0][0] == password:
                return True, uid[0][0]
            else:
                return False, None
        return False, None

    def check_user_love_exist(self, uid, mid):
        id = self.mysql.select_id_from_user_love(uid, mid)
        if id:
            return True
        else:
            return False

    def check_user_music_exist(self, uid, mid):
        id = self.mysql.select_id_from_user_music(uid, mid)
        if id:
            return True
        else:
            return False

    def insert_buy_log_to_user_music(self, uid, mid):
        state = self.mysql.insert_into_user_music(uid, mid)
        return state  # True or False

    def insert_love_log_to_user_music(self, uid, mid):
        state = self.mysql.insert_into_user_love(uid, mid)
        return state  # True or False

    def insert_playlist_to_playlist(self, pid, p_name, uid, mid):
        state = self.mysql.insert_into_playlist(pid, p_name, uid, mid)
        return state

    def insert_item_into_w_playlist(self, p_name, uid):
        pid = self.mysql.insert_into_w_playlist_and_return_pid(p_name, uid)
        if pid == 0 or pid:
            return pid[0][0]
        return None

    def update_music_all_buy_num(self, mid):
        self.mysql.update_music_all(mid)

# def test():
#     a = MysqlMusic()
#     b = a.get_playlist_all_music(1, 'asdf')
# test()