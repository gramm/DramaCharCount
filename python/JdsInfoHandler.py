import concurrent.futures
import csv
import sys

from python.DccUtils import parse_args, exception
from python.classes.JdsChar import JdsChar
from python.JdsDatabase import JdsDatabase


class JdsInfoHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()
        self.chars = self.db.get_all_chars()
        self.total_count = None

    def reset(self):
        self.db.reset_info()
        self.db.prepare_info(self.chars)

    def update_jlpt_joyo(self):
        # read jlpt/joyou levels; count number of kanji per level at the same time
        jdpt_count = {}
        with open('jlpt_kanji.csv', mode='r', encoding='utf-8') as csv_file:
            for row in csv.reader(csv_file, delimiter=';'):
                # update kanji info
                uid = ord(row[0])
                jlpt = int(row[1])
                if uid not in self.chars:
                    new_char = JdsChar(chr(uid))
                    self.chars[uid] = new_char
                    self.db.push_char(new_char)
                self.chars[uid].set_jlpt(jlpt)
                # update count of kanji per level
                if jlpt not in jdpt_count:
                    jdpt_count[jlpt] = 0
                jdpt_count[jlpt] += 1

        with open('jouyou_kanji.csv', mode='r', encoding='utf-8') as csv_file:
            for row in csv.reader(csv_file, delimiter=';'):
                uid = ord(row[0])
                jouyou = int(row[1])
                if uid not in self.chars:
                    new_char = JdsChar(chr(uid))
                    self.chars[uid] = new_char
                    self.db.push_char(new_char)
                self.chars[uid].jouyou = jouyou

        self.db.push_kanji_jlpt_joyo(self.chars)


if __name__ == "__main__":
    print("{} started".format(__file__))

    jds_info_handler = JdsInfoHandler(sys.argv[1:])

    jds_info_handler.reset()

    jds_info_handler.update_jlpt_joyo()
    # jds_info_handler.write_kanji_distance()

    print("{} ended".format(__file__))
