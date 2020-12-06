import cProfile
import csv
import re
import sys
from operator import methodcaller

from python import settings
from python.DccUtils import parse_args, is_kanji
from python.JdsDatabase import JdsDatabase
from python.classes.JdsChar import JdsChar


class JdsInfoHandler:
    def __init__(self, argv):
        self.args = parse_args(argv)
        self.db = JdsDatabase()
        self.chars = self.db.get_all_chars_with_count()
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
                self.chars[uid].jlpt = jlpt
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

    def compute_pos_dict(self, jlpt_or_jouyou):
        # sort chars by jlpt then by count
        my_dict = dict()

        for char in self.chars.values():
            if jlpt_or_jouyou is 'jlpt':
                if char.jlpt not in my_dict:
                    my_dict[char.jlpt] = []
                my_dict[char.jlpt].append(char)
            else:
                if char.jouyou not in my_dict:
                    my_dict[char.jouyou] = []
                my_dict[char.jouyou].append(char)

        for level in my_dict:
            my_dict[level].sort(key=methodcaller('count'), reverse=True)
        return my_dict

    def update_kanji_pos(self):

        # get all char count and sort by count
        self.total_count = self.db.get_count_for_drama(JdsDatabase.get_merged_drama())

        # set jlpt position
        jlpt_dict = self.compute_pos_dict('jlpt')
        position = 1
        for level in range(len(jlpt_dict) - 1, 0, -1):
            for char in jlpt_dict[level]:
                char.jlpt_pos = position
                position += 1

        # set jouyou position
        jouyou_dict = self.compute_pos_dict('jouyou')
        position = 1
        for level in range(1, len(jouyou_dict), 1):
            for char in jouyou_dict[level]:
                char.jouyou_pos = position
                position += 1

        # set jdpt position
        char_per_level = {}
        for level in range(len(jlpt_dict) - 1, 0, -1):
            char_per_level[level] = len(jlpt_dict[level])

        position = 1
        cur_level = 5
        cur_count = 0
        for char_uid in sorted(self.total_count, key=self.total_count.get, reverse=True):
            if is_kanji(self.chars[char_uid].value):
                self.chars[char_uid].jdpt_pos = position
                self.chars[char_uid].set_count(self.total_count[char_uid])
                position += 1

                if cur_level > 0:
                    self.chars[char_uid].jdpt = cur_level
                    cur_count += 1
                    if cur_count == char_per_level[cur_level]:
                        cur_count = 0
                        cur_level -= 1

        self.db.push_kanji_pos(self.chars)

    def update_kanji_flags(self):
        for char in self.chars.values():
            if is_kanji(char.value):
                char.flag = 1
            elif re.match("[ぁ-んァ-ン]", char.value):
                char.flag = 2
            else:
                char.flag = 3
        self.db.push_kanji_info_flags(self.chars)


if __name__ == "__main__":
    print("{} started".format(__file__))

    if settings.enable_profiler:
        pr = cProfile.Profile()
        pr.enable()

    jds_info_handler = JdsInfoHandler(sys.argv[1:])

    jds_info_handler.reset()

    jds_info_handler.update_jlpt_joyo()

    jds_info_handler.update_kanji_pos()

    jds_info_handler.update_kanji_flags()

    print("{} ended".format(__file__))

    if settings.enable_profiler:
        pr.disable()
        pr.print_stats(sort="cumulative")
