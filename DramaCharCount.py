import os
import sys, getopt
import time

import mysql.connector
from mysql.connector import Error
from DccUtils import *


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


def create_dramas(db, path):
    mycursor = db.cursor()
    subfolders = get_subfolders(path)
    uid = 0
    for subfolder in subfolders:
        sql = "INSERT INTO drama (drama_uid, name) VALUES('{uid}','{name}')".format(uid=uid, name=os.path.basename(subfolder))
        mycursor.execute(sql)
        uid += 1
    db.commit()
    print("Inserted {} entries in table drama".format(uid))


def count_char(db, path):
    mycursor = db.cursor()
    subfolders = get_subfolders(path)
    drama_uid = 0
    chars_uid = {}
    for subfolder in subfolders:
        chars = {}
        print("Processing {subfolder}".format(subfolder=subfolder))
        # process each file in folder
        for filepath in get_files(subfolder):
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
                        # verify if this character has a uid
                        if c not in chars_uid:
                            chars_uid[c] = len(chars_uid.keys())
        # update count for this drama
        for key, value in chars.items():
            sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES('{kanji_uid}','{drama_uid}','{count}')".format(kanji_uid=chars_uid[key], drama_uid=drama_uid, count=value)
            mycursor.execute(sql)
        # go to next drama
        drama_uid = drama_uid + 1
    # once all drama have been processed, push to database
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


if __name__ == "__main__":
    print("DramaCharCount started")
    main(sys.argv[1:])
    print("DramaCharCount successfully executed")
