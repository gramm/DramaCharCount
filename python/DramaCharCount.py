import concurrent.futures
import csv
import getopt
import os
import re
import sys
import threading
import time
import traceback

import mysql.connector
from mysql.connector import Error

from python.DccUtils import get_subfolders, get_files, escape_sql

g_maps = {}


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

    sql = "DROP TABLE IF EXISTS kanji_flag"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS line"
    mycursor.execute(sql)

    sql = "DROP TABLE IF EXISTS kanji_to_line"
    mycursor.execute(sql)

    # create tables
    sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji (kanji_uid SMALLINT PRIMARY KEY NOT NULL, value NCHAR(1))"
    mycursor.execute(sql)

    sql = "CREATE TABLE line (line_uid  SMALLINT PRIMARY KEY NOT NULL, value TEXT)"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_to_line (kanji_uid SMALLINT, line_uid SMALLINT , INDEX(kanji_uid), INDEX(line_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE count (kanji_uid SMALLINT, drama_uid SMALLINT , count INT, INDEX(kanji_uid), INDEX(drama_uid))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_info (kanji_uid SMALLINT PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT, jdpt TINYINT, dist_to_jlpt TINYINT, dist_to_jdpt TINYINT, flag TINYINT, INDEX(kanji_uid,jlpt, jouyou, jdpt, dist_to_jlpt, dist_to_jdpt,    flag))"
    mycursor.execute(sql)

    sql = "CREATE TABLE kanji_flag (id SMALLINT PRIMARY KEY NOT NULL, value VARCHAR(255), INDEX(id,value))"
    mycursor.execute(sql)

    sql = "INSERT INTO kanji_flag (id, value) VALUES (1,'Kana'),(2,'Kanji'),(3,'Unreadable')"
    mycursor.execute(sql)


def create_dramas(db, path):
    global g_maps
    drama_map = {}
    mycursor = db.cursor()
    subfolders = get_subfolders(path)
    # insert dummy drama for all drama together with uid 1
    sql = "INSERT INTO drama (drama_uid, name) VALUES('1','--> All Dramas Together <--')"
    mycursor.execute(sql)
    uid = 2  # uid 0 is reserved for all dramas together
    for subfolder in subfolders:
        drama_map[subfolder] = uid
        sql = "INSERT INTO drama (drama_uid, name) VALUES('{uid}','{name}')".format(uid=uid, name=os.path.basename(subfolder))
        mycursor.execute(sql)
        uid += 1
    db.commit()
    print("Inserted {} entries in table drama".format(uid))
    g_maps["drama_name_to_uid"] = drama_map


def count_char_work(folder, lock):
    sql = ""

    try:
        global g_maps
        print("count_char_work started on {} in thread {}".format(folder, threading.get_ident()))
        chars = {}  # key = char, value = count
        char_to_line = g_maps["char_to_lines"]
        # count chars
        for filepath in get_files(folder):
            with open(filepath, encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    for c in line:

                        try:
                            # increment count for this drama
                            if c in chars:
                                chars[c] = chars[c] + 1
                            else:
                                chars[c] = 1
                            if c not in char_to_line:
                                with lock:
                                    if c not in char_to_line:  # map might have been concurrently changed since test
                                        char_to_line[c] = []
                            if len(char_to_line[c]) < 10:
                                with lock:
                                    if len(char_to_line[c]) < 10:  # map might have been concurrently changed since test
                                        char_to_line[c].append(line)
                        except Exception as e:
                            exception(e)
        # update chars_uid map
        if "\n" in chars:
            del chars["\n"]
        chars_uid = g_maps["char_to_uid"]
        uid_char = g_maps["uid_to_char"]
        drama_uid = g_maps["drama_name_to_uid"][folder]
        sql_inserts = []

        for char, count in chars.items():
            if char not in chars_uid:
                with lock:
                    if char not in chars_uid:
                        chars_uid[char] = len(chars_uid.keys()) + 1
                        uid_char[chars_uid[char]] = char
            sql_insert = "({},{},{})".format(chars_uid[char], drama_uid, count)
            sql_inserts.append(sql_insert)

        for char, count in chars.items():
            if char not in chars_uid:
                raise Exception('char not in uid : ')
        # use batch insert
        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
    except Exception as e:
        exception(e)
    print("count_char_work exited on {} in thread {}".format(folder, threading.get_ident()))
    return sql


def count_and_upload_char(db, path):
    global g_maps
    lock = threading.Lock()
    mycursor = db.cursor(dictionary=True)
    # create char to uid map
    g_maps["char_to_uid"] = {}
    g_maps["uid_to_char"] = {}
    g_maps["char_to_lines"] = {}
    g_maps["char_uid_to_count"] = {}

    subfolders = get_subfolders(path)

    # count chars in each drama (multithreaded). Each drama uploads its own count in its own thread.
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for subfolder in subfolders:
            futures[subfolder] = executor.submit(count_char_work, subfolder, lock)
        for future in concurrent.futures.as_completed(futures.values()):
            sql = future.result()
            try:
                mycursor.execute(sql)
            except Exception as e:
                print(sql)
                exception(e)

    # upload uids
    sql_inserts = []
    for char, uid in g_maps["char_to_uid"].items():
        sql_insert = "({},\'{}\')".format(uid, escape_sql(char))
        sql_inserts.append(sql_insert)

    sql = "INSERT INTO kanji (kanji_uid, value) VALUES {}".format(",".join(sql_inserts))
    mycursor.execute(sql)
    db.commit()

    # upload total count by fetching the count of all dramas from database, summing the values, the uploading with drama uid 1
    total_count = g_maps["char_uid_to_count"]
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
    mycursor.execute(sql)
    ## csv output (optional)
    # uid_to_char = {}
    # for char, uid in g_maps["char_to_uid"].items():
    #    uid_to_char[uid] = char
    # f = open('C:/Users/Max/Documents/_tmp/count.csv', 'w', encoding="utf-8", newline='')
    # with f:
    #    writer = csv.writer(f)
    #    for char_uid, count in total_count.items():
    #        if re.match("[一-龯]", uid_to_char[char_uid]):
    #            writer.writerow([uid_to_char[char_uid], count])


def write_kanji_distance(db):
    # this function is a monster and should be rewritten by having a class for kanji and working with the kanji attributes instead of nesting dicts for ever
    total_count = g_maps["char_uid_to_count"]
    uid_to_char = g_maps["uid_to_char"]
    jdpt_level = g_maps["char_uid_to_jdpt"]
    jlpt_level = g_maps["char_uid_to_jlpt"]

    g_maps["distance_jdtp_to_jlpt"] = {}
    g_maps["distance_jltp_to_jdpt"] = {}
    distance_jdtp_to_jlpt = g_maps["distance_jdtp_to_jlpt"]
    distance_jltp_to_jdpt = g_maps["distance_jltp_to_jdpt"]


    # create nested dicts (1st dict is direction, 2nd dict is level, 3rd dict is distance/count value as tring to write in javascrip var)
    jouyou_level = g_maps["char_uid_to_jouyou"]
    distance = {"jdpt_to_jlpt": {}, "jlpt_to_jdpt": {}}
    labels = {"jdpt_to_jlpt": {}, "jlpt_to_jdpt": {}}

    for i in range(1, 6):
        distance["jdpt_to_jlpt"][i] = {}
        distance["jlpt_to_jdpt"][i] = {}
        labels["jdpt_to_jlpt"][i] = {}
        labels["jlpt_to_jdpt"][i] = {}

    # classify each kanji by level then by distance.
    for char_uid in jdpt_level.keys():
        cur_jdpt_level = jdpt_level[char_uid] if char_uid in jdpt_level else 0
        cur_jlpt_level = jlpt_level[char_uid] if char_uid in jlpt_level else 0
        count = total_count[char_uid]

        if count > 10000:
            count = int(int(round(count/10000)) * 10000)
        if count > 1000:
            count = int(int(round(count/1000)) * 1000)
        if count > 100:
            count = int(int(round(count/100)) * 100)
        elif count > 10:
            count = int(int(round(count / 10)) * 10)
        else:
            count = round(count / 10) * 10
            if count == 0:
                count = 1

        if cur_jdpt_level is not 0:
            cur_distance = cur_jdpt_level - cur_jlpt_level
            if cur_distance not in distance["jdpt_to_jlpt"][cur_jdpt_level]:
                distance["jdpt_to_jlpt"][cur_jdpt_level][cur_distance] = {}
            if count not in distance["jdpt_to_jlpt"][cur_jdpt_level][cur_distance]:
                distance["jdpt_to_jlpt"][cur_jdpt_level][cur_distance][count] = []  # list of all char_ui labels for this coordinate (x=distance, y=count)
            distance["jdpt_to_jlpt"][cur_jdpt_level][cur_distance][count].append(uid_to_char[char_uid])
        #if cur_jlpt_level is not 0:
        #    cur_distance = cur_jlpt_level - cur_jdpt_level
        #    distance["jlpt_to_jdpt"][cur_jlpt_level][char_uid] = "{{x:{},y:{}}}".format(cur_distance, count)  # x = distance, y = count
        #    labels["jlpt_to_jdpt"][cur_jlpt_level][char_uid] = "'{}'".format(uid_to_char[char_uid])
        #    distance_jltp_to_jdpt[char_uid] = cur_distance

    file_content = ["<script>\n\n"]
    for level in range(1, 6):
        points = []
        labels = []
        # generate points
        for cur_distance in distance["jdpt_to_jlpt"][level].keys():
            for cur_count in distance["jdpt_to_jlpt"][level][cur_distance]:
                points.append("{{x:{},y:{}}}".format(cur_distance, cur_count))
                chars = []
                for char in distance["jdpt_to_jlpt"][level][cur_distance][cur_count]:
                    chars.append(char)
                labels.append(" ".join(chars))
        new_data = "var jdpt_{}_to_jlpt_data =[DATA];".format(level).replace("DATA", ",".join(points), 1)
        new_labels = "var jdpt_{}_to_jlpt_label =[\'LABELS\'];".format(level).replace("LABELS", '\',\''.join(labels), 1)
        file_content.append(new_data)
        file_content.append(new_labels)
#        new_data = "var jlpt_{}_to_jdpt_data =[DATA];".format(level).replace("DATA", ",".join(distance["jlpt_to_jdpt"][level].values()), 1)
#        new_labels = "var jlpt_{}_to_jdpt_label =[LABELS];".format(level).replace("LABELS", ",".join(labels["jlpt_to_jdpt"][level].values()), 1)
#        file_content.append(new_data)
#        file_content.append(new_labels)
#
    file_content.append("\n</script>")

    f = open('C:/Users/Max/Documents/My Documents/PythonWorkspace/DramaCharCount/web/public_html/jdpt/jdpt_jlpt_dist.js', 'w', encoding="utf-8")
    with f:
        writer = f.write("\n".join(file_content))

def load_dicts():
    global g_maps
    char_to_uid = g_maps["char_to_uid"]

    # update dict
    g_maps["char_uid_to_jlpt"] = {}
    g_maps["char_uid_to_jdpt"] = {}
    g_maps["char_uid_to_jouyou"] = {}

    jlpt_level = g_maps["char_uid_to_jlpt"]
    jdpt_level = g_maps["char_uid_to_jdpt"]
    jouyou_level = g_maps["char_uid_to_jouyou"]

    # read jlpt/joyou levels
    with open('jlpt_kanji.csv', mode='r', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=';'):
            if row[0] in char_to_uid:
                jlpt_level[char_to_uid[row[0]]] = int(row[1])

    with open('jouyou_kanji.csv', mode='r', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file, delimiter=';'):
            if row[0] in char_to_uid:
                jouyou_level[char_to_uid[row[0]]] = int(row[1])

    # create JDPT ranking
    jdpt_count = {}
    for value in jlpt_level.values():
        value = value
        if value not in jdpt_count:
            jdpt_count[value] = 1
        else:
            jdpt_count[value] += 1

    # create count
    total_count = g_maps["char_uid_to_count"]
    cur_jdpt_level = len(jdpt_count)
    counter = 0
    for char_uid in sorted(total_count, key=total_count.get, reverse=True):
        if not is_kanji(g_maps["uid_to_char"][char_uid]):
            continue
        jdpt_level[char_uid] = cur_jdpt_level
        counter += 1
        if cur_jdpt_level > 0:
            if counter >= jdpt_count[cur_jdpt_level]:
                counter = 0
                cur_jdpt_level -= 1


def update_kanji_info(db):
    global g_maps

    jlpt_level = g_maps["char_uid_to_jlpt"]
    jdpt_level = g_maps["char_uid_to_jdpt"]
    jouyou_level = g_maps["char_uid_to_jouyou"]
    distance_jdtp_to_jlpt = g_maps["distance_jdtp_to_jlpt"]
    distance_jltp_to_jdpt = g_maps["distance_jltp_to_jdpt"]

    sql_inserts = []
    for value, kanji_uid in g_maps["char_to_uid"].items():
        cur_jlpt_level = jlpt_level[kanji_uid] if kanji_uid in jlpt_level else 0
        cur_jouyou_level = jouyou_level[kanji_uid] if kanji_uid in jouyou_level else 0
        cur_jdpt_level = jdpt_level[kanji_uid] if kanji_uid in jdpt_level else 0
        cur_distance_jdtp_to_jlpt = distance_jdtp_to_jlpt[kanji_uid] if kanji_uid in distance_jdtp_to_jlpt else 99
        cur_distance_jltp_to_jdpt = distance_jltp_to_jdpt[kanji_uid] if kanji_uid in distance_jltp_to_jdpt else 99

        flag = 0
        if is_kanji(value):
            flag = 1
        elif re.match("[ぁ-んァ-ン]", value):
            flag = 2
        else:
            flag = 3
        sql_insert = "({},{},{},{},{},{},{})".format(kanji_uid, cur_jlpt_level, cur_jouyou_level, cur_jdpt_level, cur_distance_jdtp_to_jlpt, cur_distance_jltp_to_jdpt, flag)
        sql_inserts.append(sql_insert)
    sql = "INSERT INTO kanji_info (kanji_uid, jlpt, jouyou, jdpt, dist_to_jlpt, dist_to_jdpt, flag) VALUES {}".format(",".join(sql_inserts))
    mycursor = db.cursor()
    mycursor.execute(sql)
    db.commit()


def upload_lines(db):
    global g_maps
    char_to_line = g_maps["char_to_lines"]
    char_to_uid = g_maps["char_to_uid"]
    line_to_uid = {}

    # upload line values
    for lines in char_to_line.values():
        for line in lines:
            if line not in line_to_uid:
                line_to_uid[line] = len(line_to_uid.keys()) + 1

    sql_inserts = []
    for line, uid in line_to_uid.items():
        line = escape_sql(line)
        sql_insert = "({},'{}')".format(uid, line)
        sql_inserts.append(sql_insert)
        # this request will be probably be over max_allowed_packet, so we update by batches of 5000 kanji
        if len(sql_inserts) > 5000:
            sql = "INSERT INTO line (line_uid, value) VALUES {}".format(",".join(sql_inserts))
            sql = sql.replace("\n", "")
            mycursor = db.cursor()
            mycursor.execute(sql)
            db.commit()
            sql_inserts.clear()
    if len(sql_inserts) > 0:
        sql = "INSERT INTO line  (line_uid, value) VALUES {}".format(",".join(sql_inserts))
        sql = sql.replace("\n", "")
        mycursor = db.cursor()
        mycursor.execute(sql)
        db.commit()

    # upload char to line reference
    sql_inserts = []
    for char, lines in char_to_line.items():
        if char is "\n":
            continue
        for line in lines:
            sql_insert = "({},{})".format(char_to_uid[char], line_to_uid[line])
            sql_inserts.append(sql_insert)
    sql = "INSERT INTO kanji_to_line (kanji_uid, line_uid) VALUES {}".format(",".join(sql_inserts))
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
    count_and_upload_char(db, args["path"])
    stop_time = time.time()
    print("count_char in {:2.3f} seconds".format(stop_time - start_time))

    start_time = time.time()
    upload_lines(db)
    stop_time = time.time()
    print("upload_lines in {:2.3f} seconds".format(stop_time - start_time))

    load_dicts()
    start_time = time.time()
    write_kanji_distance(db)
    stop_time = time.time()
    print("write_kanji_distance in {:2.3f} seconds".format(stop_time - start_time))

    start_time = time.time()
    update_kanji_info(db)
    stop_time = time.time()
    print("update_kanji_info in {:2.3f} seconds".format(stop_time - start_time))


if __name__ == "__main__":
    print("DramaCharCount started")
    main(sys.argv[1:])
    print("DramaCharCount successfully executed")
