import concurrent.futures
import csv
import re
import sys
import threading
from logging import exception

import mysql
from mysql.connector import Error

from python.DccUtils import parse_args, load_dramas, get_subfolders, escape_sql, get_files

from sudachipy import tokenizer
from sudachipy import dictionary

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

    def count_word_work(self, folder, lock):
        sql = ""

        tokenizer_obj = dictionary.Dictionary().create()
        mode = tokenizer.Tokenizer.SplitMode.A

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
            sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
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
        g_maps["char_uid_to_count"] = {}

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

        sql = "INSERT INTO kanji (kanji_uid, value) VALUES {}".format(",".join(sql_inserts))
        if self.db:
            mycursor.execute(sql)
            self.db.commit()

        # upload total count by fetching the count of all dramas from database, summing the values, the uploading with drama uid 1
        total_count = g_maps["char_uid_to_count"]
        if self.db:
            mycursor.execute("SELECT * FROM count")
        for result in mycursor.fetchall():
            kanji_uid = result["kanji_uid"]
            count = result["count"]
            if kanji_uid not in total_count:
                total_count[kanji_uid] = count
            else:
                total_count[kanji_uid] = total_count[kanji_uid] + count

        sorted(total_count.items(), key=lambda x: x[1], reverse=True)  # sort total_count by values descencding i.e. by count

        sql_inserts = []
        for char_uid, count in total_count.items():
            sql_insert = "({},{},{})".format(char_uid, 1, count)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))

        if self.db:
            mycursor.execute(sql)

        # csv output (optional)
        uid_to_word = {}
        for char, uid in g_maps["word_to_uid"].items():
            uid_to_word[uid] = char
        f = open('C:/Users/Max/Documents/_tmp/count.csv', 'w', encoding="utf-8", newline='')
        with f:
            writer = csv.writer(f)
            for char_uid, count in total_count.items():
                writer.writerow([uid_to_word[char_uid], count])
                # if re.match("[一-龯]", uid_to_word[char_uid]):


if __name__ == "__main__":
    print("DramaWordCount started")

    dwc = DramaWordCount()
    dwc.parse_args(sys.argv[1:])
    dwc.connect()
    dwc.load_dramas()
    dwc.count_and_upload_words()

    print("DramaWordCount successfully executed")
