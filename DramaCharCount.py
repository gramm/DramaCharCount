import concurrent.futures
import csv
import getopt
import sys
import threading
import time

import mysql.connector
from mysql.connector import Error

from DccUtils import *

uid_maps = {}


def parse_args(argv):
    """
    Parse the arguments for MySql connection
    :param argv:
    :return:
    """
    ret_dict = {
        "sql_host": "",
        "sql_user": "",
        "sql_password": "",
        "sql_database": "",
        "path": ""
    }
    try:
        opts, args = getopt.getopt(argv, "h:u:pw:db:pa", ["host=", "user=", "password=", "database=", "path="])
    except getopt.GetoptError as err:
        print("Could not parse program arguments")
        print(str(err))  # will print something like "option -a not recognized"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--host'):
            ret_dict["sql_host"] = arg
            print("sql_host = {}".format(ret_dict["sql_host"]))
        elif opt in ('-u', '--user'):
            ret_dict["sql_user"] = arg
            print("sql_user = {}".format(ret_dict["sql_user"]))
        elif opt in ('-pw', '--password'):
            ret_dict["sql_password"] = arg
            print("sql_password = {}".format(ret_dict["sql_password"]))
        elif opt in ('-db', '--database'):
            ret_dict["sql_database"] = arg
            print("sql_database = {}".format(ret_dict["sql_database"]))
        elif opt in ('-pa', '--path'):
            ret_dict["path"] = arg
            print("path = {}".format(ret_dict["path"]))
        else:
            print("Unknown argument {}".format(opt))
            sys.exit(2)

    for key, value in ret_dict.items():
        if not value:
            print("Missing command line arguments {}".format(key))
            sys.exit(2)
    return ret_dict


def reset_tables(db):
    mycursor = db.cursor()

    # drop all tables
    sql = "DROP TABLE IF EXISTS count"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS drama"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji_info"
    mycursor.execute(sql)

    # create tables
    sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji (kanji_uid SMALLINT PRIMARY KEY NOT NULL, value NCHAR(1))"
    mycursor.execute(sql)

    sql = "CREATE TABLE count (kanji_uid SMALLINT, drama_uid SMALLINT , count INT, INDEX(kanji_uid), INDEX(drama_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_info (kanji_uid SMALLINT PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT)"
    mycursor.execute(sql)


def create_dramas(db, path):
    global uid_maps
    drama_map = {}
    mycursor = db.cursor()
    subfolders = get_subfolders(path)
    uid = 0
    for subfolder in subfolders:
        drama_map[subfolder] = uid
        sql = "INSERT INTO drama (drama_uid, name) VALUES('{uid}','{name}')".format(uid=uid, name=os.path.basename(subfolder))
        mycursor.execute(sql)
        uid += 1
    db.commit()
    print("Inserted {} entries in table drama".format(uid))
    uid_maps["drama_uid"] = drama_map


def count_char_work(folder):
    sql = ""
    try:
        global uid_maps
        print("count_char_work started on {} in thread {}".format(folder, threading.get_ident()))
        chars = {}
        # count chars
        for filepath in get_files(folder):
            with open(filepath, encoding='utf-8') as file:
                data = file.read()
                for c in data:
                    if not c:
                        # end of file
                        break
                    else:
                        # increment count for this drama
                        if c in chars:
                            chars[c] = chars[c] + 1
                        else:
                            chars[c] = 1
        # update chars_uid map
        del chars["\n"]
        chars_uid = uid_maps["chars_uid"]
        drama_uid = uid_maps["drama_uid"][folder]
        sql_inserts = []
        for char, count in chars.items():
            if char not in chars_uid:
                chars_uid[char] = len(chars_uid.keys())
            sql_insert = "({},{},{})".format(chars_uid[char], drama_uid, count)
            sql_inserts.append(sql_insert)
        # use batch insert
        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
    except Exception as e:
        print(e)
    return sql


def count_char(db, path):
    global uid_maps
    mycursor = db.cursor()
    # create char to uid map
    uid_maps["chars_uid"] = {}

    subfolders = get_subfolders(path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for subfolder in subfolders:
            futures[subfolder] = executor.submit(count_char_work, subfolder)
        for future in concurrent.futures.as_completed(futures.values()):
            mycursor.execute(future.result())
    # upload uids
    sql_inserts = []
    for char, uid in uid_maps["chars_uid"].items():
        sql_insert = "({},\"{}\")".format(uid, char)
        sql_inserts.append(sql_insert)

    sql = "INSERT INTO kanji (kanji_uid, value) VALUES {}".format(",".join(sql_inserts))
    sql = sql.replace("\"\"\"", "\"\\\"\"", 1)  # replace """ with "\"" as " is a special char in mysql
    mycursor.execute(sql)

    db.commit()


def update_kanji_info(db):
    global uid_maps
    jlpt_level = {}
    jouyou_level = {}

    with open('jlpt_kanji.csv', mode='r', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=';'):
            jlpt_level[row[0]] = row[1]

    with open('jouyou_kanji.csv', mode='r', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=';'):
            jouyou_level[row[0]] = row[1]

    sql_inserts = []
    for value, kanji_uid in uid_maps["chars_uid"].items():
        sql_insert = "({},{},{})".format(kanji_uid, jlpt_level[value] if value in jlpt_level else 0, jouyou_level[value] if value in jouyou_level else 0)
        sql_inserts.append(sql_insert)
    sql = "INSERT INTO kanji_info (kanji_uid, jlpt, jouyou) VALUES {}".format(",".join(sql_inserts))
    mycursor = db.cursor()
    mycursor.execute(sql)
    db.commit()


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

    start_time = time.time()
    create_dramas(db, args["path"])
    stop_time = time.time()
    print("create_dramas in {:2.3f} seconds".format(stop_time - start_time))

    start_time = time.time()
    count_char(db, args["path"])
    stop_time = time.time()
    print("count_char in {:2.3f} seconds".format(stop_time - start_time))

    start_time = time.time()
    update_kanji_info(db)
    stop_time = time.time()
    print("update_kanji_info in {:2.3f} seconds".format(stop_time - start_time))


if __name__ == "__main__":
    print("DramaCharCount started")
    main(sys.argv[1:])
    print("DramaCharCount successfully executed")
