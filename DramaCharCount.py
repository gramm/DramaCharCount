import os
import sys, getopt
import mysql.connector
from mysql.connector import Error


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
        # print help information and exit:
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

    sql = "DROP TABLE IF EXISTS count"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS drama"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji_info"
    mycursor.execute(sql)

    sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji (kanji_uid SMALLINT PRIMARY KEY NOT NULL, value NCHAR(1))"
    mycursor.execute(sql)

    sql = "CREATE TABLE count (kanji_uid SMALLINT, drama_uid SMALLINT , count INT, INDEX(kanji_uid), INDEX(drama_uid))"
    mycursor.execute(sql)


def count_char(db, path):
    pass


def create_dramas(db, path):
    mycursor = db.cursor()
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    uid = 0
    for subfolder in subfolders:
        sql = "INSERT INTO drama (drama_uid, name) VALUES('{uid}','{name}')".format(uid=uid, name=os.path.basename(subfolder))
        print(sql)
        mycursor.execute(sql)
        uid += 1
    db.commit()
    print("Inserted {} entries in table drama".format(uid))


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

    create_dramas(db, args["path"])
    count_char(db, args["path"])


if __name__ == "__main__":
    print("DramaCharCount started")
    main(sys.argv[1:])
    print("DramaCharCount successfully executed")
