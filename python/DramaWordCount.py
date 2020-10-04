import sys

import mysql
from mysql.connector import Error

from python.DccUtils import parse_args, load_dramas

g_maps = {}


class DramaWordCount:

    def __init__(self):
        self.args = {}
        pass

    def parse_args(self, argv):
        self.args = parse_args(argv)

    def connect(self):
        try:
            db = mysql.connector.connect(
                host=self.args["sql_host"],
                database=self.args["sql_database"],
                user=self.args["sql_user"],
                password=self.args["sql_password"],
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
            sys.exit(2)

        if db.is_connected():
            print("Database connection successful")
        else:
            print("Could not connect to database, exiting...")
            sys.exit(2)

    def load_dramas(self):
        g_maps["drama_name_to_uid"] = load_dramas(self.args["path"])


if __name__ == "__main__":
    print("DramaWordCount started")
    dwc = DramaWordCount()
    dwc.parse_args(sys.argv[1:])
    dwc.connect()
    print("DramaWordCount successfully executed")
