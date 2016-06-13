# -*- coding: utf-8 -*-

import MySQLdb as mdb


class MySql(object):
    def __init__(self):
        super().__init__()
        self.con = mdb.connect('localhost', 'ling', 'ling000', 'music', charset="utf8");
        self.cur = self.con.cursor()
        self.cur.execute("SET NAMES utf8")

    def insert_into_c_user(self, name, password, permit):
        # name max len 10, str
        # password max len 25, str
        # right int
        try:
            self.cur.execute("INSERT INTO C_User (username, password, permit) "
                             "VALUE('{}', '{}', '{}')".format(name, password, permit))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def insert_into_music_all(self, mid, title, artists, url, m_length, album, buy_num):
        try:
            self.cur.execute("INSERT INTO Music_All (mid, title, artists, url,"
                             "m_length, album, buy_num) "
                             "VALUE('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                             .format(mid, title, artists, url, m_length, album, buy_num))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def insert_into_user_music(self, uid, mid):
        try:
            self.cur.execute("INSERT INTO User_Music (uid, mid) "
                             "VALUE('{}', '{}')".format(uid, mid))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def insert_into_user_love(self, uid, mid):
        try:
            self.cur.execute("INSERT INTO User_Love (uid, mid)"
                             " VALUE ('{}', '{}')".format(uid, mid))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def insert_into_playlist(self, pid, p_name, uid, mid):
        try:
            self.cur.execute("INSERT INTO Playlist (pid, p_name, uid, mid)"
                             "VALUE('{}', '{}', '{}', '{}')"
                             .format(pid, p_name, uid, mid))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def insert_into_w_playlist_and_return_pid(self, p_name, uid):
        try:
            self.cur.execute("INSERT INTO W_playlist (p_name, uid, publish)"
                             "VALUE('{}', '{}', '0')"
                             .format(p_name, uid))
            self.cur.execute("SELECT pid FROM W_playlist WHERE "
                             " uid='{}' AND p_name='{}'".format(uid, p_name))
            self.con.commit()
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def rebuild_rank(self):
        self.cur.execute("DROP TABLE IF EXISTS rank")
        self.cur.execute("CREATE TABLE rank(mid INT , url VARCHAR(300)) "
                         "default character set utf8 collate utf8_general_ci")
        self.con.commit()

    def insert_music_into_rank(self, mid, url):
        try:
            self.cur.execute("INSERT INTO rank (mid, url) VALUE('{}', '{}')".format(mid, url))
            self.con.commit()
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            self.con.rollback()
            return False

    def select_uid_from_c_user(self, username):
        self.cur.execute("SELECT uid FROM C_User WHERE "
                         "username='{}'".format(username))
        return self.cur.fetchall()

    def select_password_from_c_user(self, username):
        self.cur.execute("SELECT password FROM C_User WHERE"
                         " username='{}'".format(username))
        return self.cur.fetchall()

    def select_username_from_c_user(self, uid):
        self.cur.execute("SELECT username FROM C_User WHERE "
                         "uid='{}'".format(uid))
        return self.cur.fetchall()

    def select_mid_url_from_music_all(self):
        num = self.cur.execute("SELECT mid, url FROM Music_All")
        return self.cur.fetchall(), num

    def select_mid_from_user_music(self, uid):
        num = self.cur.execute("SELECT mid FROM User_Music "
                               "WHERE uid='{}'".format(uid))
        return self.cur.fetchall(), num

    def select_mid_from_user_love(self, uid):
        num = self.cur.execute("SELECT mid FROM User_Love "
                               "WHERE uid='{}'".format(uid))
        return self.cur.fetchall(), num

    def select_url_from_music_all(self, mid):
        self.cur.execute("SELECT url FROM Music_All"
                         " WHERE mid='{}'".format(mid))
        return self.cur.fetchall()

    def select_id_from_user_love(self, uid, mid):
        self.cur.execute("SELECT like_id FROM User_Love "
                         "WHERE uid='{}' and mid='{}'".format(uid, mid))
        return self.cur.fetchall()

    def select_id_from_user_music(self, uid, mid):
        self.cur.execute("SELECT order_id FROM User_Music "
                         "WHERE uid='{}' and mid='{}'".format(uid, mid))
        return self.cur.fetchall()

    def select_all_from_w_playlist(self, uid):
        num = self.cur.execute("SELECT pid, p_name, publish FROM W_playlist"
                               " WHERE uid='{}'".format(uid))
        return self.cur.fetchall(), num

    def select_playlist_from_w_playlist(self):
        num = self.cur.execute("SELECT pid, p_name FROM W_playlist WHERE "
                               "publish='0'")
        return self.cur.fetchall(), num

    def select_mid_from_playlist(self, pid, p_name):
        num = self.cur.execute("SELECT mid FROM Playlist WHERE pid='{}' AND "
                               "p_name='{}'".format(pid, p_name))
        return self.cur.fetchall(), num

    def select_rank_from_music_all(self):
        self.cur.execute("select * from Music_All order by buy_num")
        return self.cur.fetchall()

    def select_music_from_rank(self):
        self.cur.execute("SELECT * FROM rank")
        return self.cur.fetchall()

    def update_music_all(self, mid):
        self.cur.execute("UPDATE Music_All SET buy_num=buy_num + 1 "
                         "WHERE mid='{}'".format(mid))
        self.con.commit()

    def update_w_playlist(self, pid):
        self.cur.execute("UPDATE W_playlist SET publish=1 WHERE pid='{}'"
                         .format(pid))
        self.con.commit()