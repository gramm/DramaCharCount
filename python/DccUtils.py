import getopt
import os
import re
import sys
import traceback

from python import settings


def get_subfolders(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]


def get_files(path):
    retlist = []
    for root, subFolder, files in os.walk(path):
        for item in files:
            retlist.append((os.path.join(root, item)))
    return retlist


def is_kanji(c):
    return re.match("[一-龯]", c)


def exception(e):
    if hasattr(e, 'message'):
        print(e.message)
    else:
        print(e)
    traceback.print_exc()


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
    if not argv:  # if no arg return from settings.py
        ret_dict["sql_host"] = settings.connection_info['host']
        ret_dict["sql_database"] = settings.connection_info['database']
        ret_dict["sql_user"] = settings.connection_info['user']
        ret_dict["sql_password"] = settings.connection_info['password']
        ret_dict["path"] = settings.subtitles_path
        return ret_dict
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
            print("sql_password = ?")  # .format(ret_dict["sql_password"]))
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
            # sys.exit(2)
    return ret_dict


def is_readable(val):
    return re.search("[一-龠]+|[ぁ-ゔ]+|[ァ-ヴー]+|[a-zA-Z]+|[ａ-ｚＡ-Ｚ]+|[々〆〤]+", val)
