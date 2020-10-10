import concurrent.futures
import csv
import re
import sys
import threading
from logging import exception

import mysql
from mysql.connector import Error

from python.DccUtils import parse_args, load_dramas, get_subfolders, escape_sql, get_files, is_readable

from sudachipy import tokenizer
from sudachipy import dictionary

from python.DramaCharCount import is_kanji

g_maps = {}


class DramaWordCount:

    def __init__(self):
        self.args = {}
        self.db = None
        pass

    def parse_args(self, argv):
        self.args = parse_args(argv)

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host=self.args["sql_host"],
                database=self.args["sql_database"],
                user=self.args["sql_user"],
                password=self.args["sql_password"],
                connection_timeout=0.1
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
            return
            # sys.exit(2)

        if self.db.is_connected():
            print("Database connection successful")
        else:
            print("Could not connect to database, exiting...")
            return
            # sys.exit(2)

    def load_dramas(self):
        g_maps["drama_name_to_uid"] = load_dramas(self.args["path"])

    @staticmethod
    def count_word_work(folder, lock):
        sql = ""

        tokenizer_obj = dictionary.Dictionary().create()
        mode = tokenizer.Tokenizer.SplitMode.C

        try:
            global g_maps
            print("count_word_work started on {} in thread {}".format(folder, threading.get_ident()))
            words = {}  # key = char, value = count
            word_to_line = g_maps["word_to_lines"]
            # count chars
            for filepath in get_files(folder):
                print(filepath)
                with open(filepath, encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        try:
                            for token in tokenizer_obj.tokenize(line, mode):
                                c = token.normalized_form()
                                try:
                                    # increment count for this drama
                                    if c in words:
                                        words[c] = words[c] + 1
                                    else:
                                        words[c] = 1
                                    if c not in word_to_line:
                                        with lock:
                                            if c not in word_to_line:  # map might have been concurrently changed since test
                                                word_to_line[c] = []
                                    if len(word_to_line[c]) < 10:  # 10 -> for the moment only keep 10 example lines per char
                                        with lock:
                                            if len(word_to_line[c]) < 10:  # map might have been concurrently changed since test
                                                word_to_line[c].append(line)
                                except Exception as e:
                                    exception(e)
                        except Exception as e:
                            exception(e)
            # update words_uid map
            if "\n" in words:
                del words["\n"]
            words_uid = g_maps["word_to_uid"]
            uid_word = g_maps["uid_to_word"]
            drama_uid = g_maps["drama_name_to_uid"][folder]
            sql_inserts = []

            for char, count in words.items():
                if char not in words_uid:
                    with lock:
                        if char not in words_uid:
                            words_uid[char] = len(words_uid.keys()) + 1
                            uid_word[words_uid[char]] = char
                sql_insert = "({},{},{})".format(words_uid[char], drama_uid, count)
                sql_inserts.append(sql_insert)

            for char, count in words.items():
                if char not in words_uid:
                    raise Exception('char not in uid : ')
            # use batch insert
            sql = "INSERT INTO count_word (word_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
        except Exception as e:
            exception(e)
        print("count_word_work exited on {} in thread {}".format(folder, threading.get_ident()))
        return sql

    def count_and_upload_words(self):
        global g_maps
        lock = threading.Lock()
        path = self.args["path"]

        if self.db:
            mycursor = self.db.cursor(dictionary=True)
        # create char to uid map
        g_maps["word_to_uid"] = {}
        g_maps["uid_to_word"] = {}
        g_maps["word_to_lines"] = {}
        g_maps["word_uid_to_count"] = {}

        subfolders = get_subfolders(path)

        # count chars in each drama (multithreaded). Each drama uploads its own count in its own thread.
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}
            for subfolder in subfolders:
                futures[subfolder] = executor.submit(self.count_word_work, subfolder, lock)
            for future in concurrent.futures.as_completed(futures.values()):
                sql = future.result()
                try:
                    if self.db:
                        mycursor.execute(sql)
                except Exception as e:
                    print(sql)
                    exception(e)

        # upload uids
        sql_inserts = []
        for char, uid in g_maps["word_to_uid"].items():
            sql_insert = "({},\'{}\')".format(uid, escape_sql(char))
            sql_inserts.append(sql_insert)

        sql = "INSERT INTO word (word_uid, value) VALUES {}".format(",".join(sql_inserts))
        if self.db:
            mycursor.execute(sql)
            self.db.commit()

        # upload total count by fetching the count of all dramas from database, summing the values, the uploading with drama uid 1
        total_count = g_maps["word_uid_to_count"]
        if self.db:
            mycursor.execute("SELECT * FROM count_word")
        for result in mycursor.fetchall():
            word_uid = result["word_uid"]
            count = result["count"]
            if word_uid not in total_count:
                total_count[word_uid] = count
            else:
                total_count[word_uid] = total_count[word_uid] + count

        sorted(total_count.items(), key=lambda x: x[1], reverse=True)  # sort total_count by values descencding i.e. by count

        sql_inserts = []
        for word_uid, count in total_count.items():
            sql_insert = "({},{},{})".format(word_uid, 1, count)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO count_word (word_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))

        if self.db:
            mycursor.execute(sql)

        # csv output (optional)
        uid_to_word = {}
        for char, uid in g_maps["word_to_uid"].items():
            uid_to_word[uid] = char
        f = open('C:/Users/Max/Documents/_tmp/count.csv', 'w', encoding="utf-8", newline='')
        with f:
            writer = csv.writer(f)
            for word_uid, count in total_count.items():
                writer.writerow([uid_to_word[word_uid], count])
                # if re.match("[一-龯]", uid_to_word[word_uid]):

    def update_word_info(self):
        global g_maps

        jlpt_level = {}#g_maps["word_uid_to_jlpt"]
        jdpt_level = {}#g_maps["word_uid_to_jdpt"]
        jouyou_level = {}#g_maps["word_uid_to_jouyou"]
        distance_jdtp_to_jlpt = {}#g_maps["distance_jdtp_to_jlpt"]
        distance_jltp_to_jdpt = {}#g_maps["distance_jltp_to_jdpt"]

        sql_inserts = []
        for value, word_uid in g_maps["word_to_uid"].items():
            cur_jlpt_level = jlpt_level[word_uid] if word_uid in jlpt_level else 0
            cur_jouyou_level = jouyou_level[word_uid] if word_uid in jouyou_level else 0
            cur_jdpt_level = jdpt_level[word_uid] if word_uid in jdpt_level else 0
            cur_distance_jdtp_to_jlpt = distance_jdtp_to_jlpt[word_uid] if word_uid in distance_jdtp_to_jlpt else 99
            cur_distance_jltp_to_jdpt = distance_jltp_to_jdpt[word_uid] if word_uid in distance_jltp_to_jdpt else 99

            flag = 0
            if is_readable(value):
                flag = 1
            elif re.match("[ぁ-んァ-ン]", value):
                flag = 2
            else:
                flag = 3

            sql_insert = "({},{},{},{},{},{},{})".format(word_uid, cur_jlpt_level, cur_jouyou_level, cur_jdpt_level, cur_distance_jdtp_to_jlpt, cur_distance_jltp_to_jdpt, flag)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO word_info (word_uid, jlpt, jouyou, jdpt, dist_to_jlpt, dist_to_jdpt, flag) VALUES {}".format(",".join(sql_inserts))
        if self.db:
            mycursor = self.db.cursor()
            mycursor.execute(sql)
            self.db.commit()


if __name__ == "__main__":
    print("DramaWordCount started")

    dwc = DramaWordCount()
    dwc.parse_args(sys.argv[1:])
    dwc.connect()
    dwc.load_dramas()
    dwc.count_and_upload_words()
    dwc.update_word_info()

    print("DramaWordCount successfully executed")
