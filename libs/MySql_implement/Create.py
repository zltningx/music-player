# -*- coding: utf-8 -*-

""" IN THIS SCRIPT WE CREATE SOME TABLE
So you should use it carefully that it will drop your tables
You can chose one to create or recreate, just active code and
run this file.
ABOUT
Music_All: Music info
C_User: User info, initial admin 'ling' password 'ling000'
User_Music: User Buy Music generation records
Playlist: User Create Playlist buy but we recorded it with\
          one pid with ont mid, so it has so many pid and mid. But \
          one pid and mid in one record must be only one!
User_Love: Like User_Music table
"""

import MySQLdb as mdb

con = mdb.connect('localhost', 'ling', 'ling000', 'music', charset="utf8");

with con:
    cur = con.cursor()
    try:
        # # Create music
        # cur.execute("DROP TABLE IF EXISTS Music_All")
        # cur.execute("CREATE TABLE Music_All (mid INT PRIMARY KEY,"
        #             "title VARCHAR(100), artists VARCHAR(30), url VARCHAR(300),"
        #             "m_length FLOAT, album  VARCHAR(100), buy_num INT)"
        #             " default character set utf8 collate utf8_general_ci")
        # # Create user
        # cur.execute("DROP TABLE IF EXISTS C_User")
        # cur.execute("CREATE TABLE C_User(uid INT PRIMARY KEY AUTO_INCREMENT,"
        #             "username VARCHAR(10), password VARCHAR(25), permit INT)"
        #             " default character set utf8 collate utf8_general_ci")
        # cur.execute("INSERT INTO C_User (username, password, permit) VALUES('{}', '{}', '{}')"
        #             .format('ling', 'ling000', 9))  # initial admin
        #
        # # Create user_music
        # cur.execute("DROP TABLE IF EXISTS User_Music")
        # cur.execute("CREATE TABLE User_Music("
        #             "order_id INT PRIMARY KEY AUTO_INCREMENT, uid INT , mid INT,"
        #             "buy_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        #             " default character set utf8 collate utf8_general_ci")
        # #
        # # Create Play_list
        # cur.execute("DROP TABLE IF EXISTS Playlist")
        # cur.execute("CREATE TABLE Playlist(pid INT, p_name VARCHAR(30),"
        #             "uid INT, mid INT)  default character set utf8 "
        #             "collate utf8_general_ci")
        # #
        # # Create Wait_play_list
        # cur.execute("DROP TABLE IF EXISTS W_playlist")
        # cur.execute("CREATE TABLE W_playlist(pid INT PRIMARY KEY AUTO_INCREMENT, "
        #             "p_name VARCHAR(30), uid INT, publish INT) "
        #             "default character set utf8 collate utf8_general_ci")
        # #
        # # Create User_love
        # cur.execute("DROP TABLE IF EXISTS User_Love")
        # cur.execute("CREATE TABLE User_Love("
        #             "like_id INT PRIMARY KEY AUTO_INCREMENT, uid INT , mid INT)"
        #             " default character set utf8 collate utf8_general_ci")
        # Create rank
        # cur.execute("DROP TABLE IF EXISTS rank")
        # cur.execute("CREATE TABLE rank(mid INT , url VARCHAR(300)) "
        #             "default character set utf8 collate utf8_general_ci")

        con.commit()
    except Exception as e:
        con.rollback()
        print(e)