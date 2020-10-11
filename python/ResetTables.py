import sys

import mysql
from mysql.connector import Error

from python.DccUtils import parse_args


def reset_tables(db):
    mycursor = db.cursor()

    # drop all tables
    sql = "DROP TABLE IF EXISTS count"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS count_word"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS drama"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji_info"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji_flag"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS word"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS word_info"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS word_flag"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS line"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji_to_line"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS word_to_line"
    mycursor.execute(sql)

    # create tables
    sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji (kanji_uid SMALLINT PRIMARY KEY NOT NULL, value NCHAR(1))"
    mycursor.execute(sql)

    sql = "CREATE TABLE word (word_uid SMALLINT PRIMARY KEY NOT NULL, value VARCHAR(255))"
    mycursor.execute(sql)

    sql = "CREATE TABLE line (line_uid  SMALLINT PRIMARY KEY NOT NULL, value TEXT)"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_to_line (kanji_uid SMALLINT, line_uid SMALLINT , INDEX(kanji_uid), INDEX(line_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE word_to_line (word_uid SMALLINT, line_uid SMALLINT , INDEX(word_uid), INDEX(line_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE count (kanji_uid SMALLINT, drama_uid SMALLINT , count INT, INDEX(kanji_uid), INDEX(drama_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE count_word (word_uid SMALLINT, drama_uid SMALLINT , count INT, INDEX(word_uid), INDEX(drama_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_info (kanji_uid SMALLINT PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT, jdpt TINYINT, dist_to_jlpt TINYINT, dist_to_jdpt TINYINT, flag TINYINT, INDEX(kanji_uid,jlpt, jouyou, jdpt, dist_to_jlpt, dist_to_jdpt,    flag))"
    mycursor.execute(sql)

    sql = "CREATE TABLE word_info (word_uid SMALLINT PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT, jdpt TINYINT, dist_to_jlpt TINYINT, dist_to_jdpt TINYINT, flag TINYINT, INDEX(word_uid,jlpt, jouyou, jdpt, dist_to_jlpt, dist_to_jdpt,    flag))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_flag (id SMALLINT PRIMARY KEY NOT NULL, value VARCHAR(255), INDEX(id,value))"
    mycursor.execute(sql)

    sql = "CREATE TABLE word_flag (id SMALLINT PRIMARY KEY NOT NULL, value VARCHAR(255), INDEX(id,value))"
    mycursor.execute(sql)

    sql = "INSERT INTO kanji_flag (id, value) VALUES (1,'Kana'),(2,'Kanji'),(3,'Unreadable')"
    mycursor.execute(sql)

    sql = "INSERT INTO word_flag (id, value) VALUES (1,'Readable'),(2,'SingleKana'),(3,'Unreadable'),(4,'One_Kana'),(5,'Excluded')"
    mycursor.execute(sql)


def main(argv):
    args = parse_args(argv)

    try:
        db = mysql.connector.connect(
            host=args["sql_host"],
            database=args["sql_database"],
            user=args["sql_user"],
            password=args["sql_password"],
        )
    except Error as e:
        print("Error while connecting to MySQL", e)
        sys.exit(2)

    if db.is_connected():
        print("Database connection successful")
    else:
        print("Could not connect to database, exiting...")
        sys.exit(2)

    reset_tables(db)


if __name__ == "__main__":
    print("ResetTables started")
    main(sys.argv[1:])
    print("ResetTables successfully executed")
