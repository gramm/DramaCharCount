import sys

import mysql
from mysql.connector import Error

from python.DccUtils import parse_args, load_dramas

from sudachipy import tokenizer
from sudachipy import dictionary

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

    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C
    [m.surface() for m in tokenizer_obj.tokenize("国家公務員", mode)]
    # => ['国家公務員']
    print(tokenizer_obj.tokenize("附属", mode)[0].normalized_form())
    # => ['国家', '公務', '員']
    #dwc = DramaWordCount()
    #dwc.parse_args(sys.argv[1:])
    #dwc.connect()
    print("DramaWordCount successfully executed")
