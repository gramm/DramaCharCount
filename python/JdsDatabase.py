from threading import Lock

import mysql
import python.settings as settings
from mysql.connector import Error

from python.DccUtils import exception
from python.classes.JdsChar import JdsChar
from python.classes.JdsDrama import JdsDrama
from python.classes.JdsLine import JdsLine


class JdsDatabase:
    __db = None
    __cursor = None
    __lock = None

    def __init__(self):
        self.max_allowed_packets = 1048576  # fixme: get from SQL (SHOW VARIABLES LIKE 'max_allowed_packet')
        pass

    @staticmethod
    def get_merged_drama():
        return JdsDrama(0, "--> All Dramas Together <--")

    @staticmethod
    def __check_state():
        if not JdsDatabase.__db:
            print(__class__.__name__ + " not connected to database")
            JdsDatabase.connect(None)
        return JdsDatabase.__db is not None

    @staticmethod
    def __escape_sql(sql):
        chars = ['\\', '\'', '\"']
        for c in chars:
            sql = sql.replace(c, '\\' + c)
        sql = sql.replace("\n", "")
        return sql

    @staticmethod
    def connect(args):
        JdsDatabase.__lock = Lock()
        if args:
            host = args["sql_host"]
            database = args["sql_database"]
            user = args["sql_user"]
            password = args["sql_password"]
        else:
            host = settings.connection_info['host']
            database = settings.connection_info['database']
            user = settings.connection_info['user']
            password = settings.connection_info['password']
        try:
            connection_timeout = 0.1
            print("Connecting {}:{}:{}".format(host, database, user))
            JdsDatabase.__db = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                connection_timeout=connection_timeout,
                charset='utf8',
                autocommit=True
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

        if JdsDatabase.__db.is_connected():
            print("Database connection successful")

            JdsDatabase.__cursor = JdsDatabase.__db.cursor(dictionary=True)

            JdsDatabase.__cursor.execute('SET NAMES utf8mb4')
            JdsDatabase.__cursor.execute("SET CHARACTER SET utf8mb4")
            JdsDatabase.__cursor.execute("SET character_set_connection=utf8mb4")
            JdsDatabase.__db.commit()
            return True
        else:
            print("Could not connect to database")
            return False

    def __cursor_execute_thread_safe(self, sql):
        if settings.print_sql:
            print(sql)
        with JdsDatabase.__lock:
            self.__cursor.execute(sql)
            self.__db.commit()
            # pass

    def __cursor_execute_fetchone_thread_safe(self, sql):
        if settings.print_sql:
            print(sql)
        with JdsDatabase.__lock:
            self.__cursor.execute(sql)
            return JdsDatabase.__cursor.fetchone()

    def __cursor_execute_fetchall_thread_safe(self, sql):
        if settings.print_sql:
            print(sql)
        with JdsDatabase.__lock:
            self.__cursor.execute(sql)
            return JdsDatabase.__cursor.fetchall()

    def __drama_from_query_result(self, result):
        drama = JdsDrama(result['drama_uid'], result['name'])
        drama.word_ok = result['word_ok']
        drama.kanji_ok = result['kanji_ok']
        drama.word_line_ref_ok = result['word_line_ref_ok']
        drama.kanji_line_ref_ok = result['kanji_line_ref_ok']
        return drama

    def get_drama(self, name_or_uid):
        if not JdsDatabase.__check_state():
            return
        if type(name_or_uid) is 'int':
            sql = "SELECT * FROM drama WHERE drama_uid='{}'".format(name_or_uid)
            result = self.__cursor_execute_fetchone_thread_safe(sql)
        else:
            sql = "SELECT * FROM drama WHERE name='{}'".format(JdsDatabase.__escape_sql(name_or_uid))
            result = self.__cursor_execute_fetchone_thread_safe(sql)

        if result:
            return self.__drama_from_query_result(result)
        else:
            return None

    def get_all_dramas(self):
        if not JdsDatabase.__check_state():
            return
        sql = "SELECT * FROM drama"
        results = self.__cursor_execute_fetchall_thread_safe(sql)
        dramas = []
        for result in results:
            dramas.append(self.__drama_from_query_result(result))
        return dramas

    def get_all_lines_by_drama(self):
        if not JdsDatabase.__check_state():
            return
        sql = "SELECT * FROM line "
        results = self.__cursor_execute_fetchall_thread_safe(sql)

        lines_by_drama = {}
        try:
            for result in results:
                if result['drama_uid'] not in lines_by_drama:
                    lines_by_drama[result['drama_uid']] = []
                lines_by_drama[result['drama_uid']].append(JdsLine(result['line_uid'], result['drama_uid'], result['value']))
        except Exception as e:
            exception(e)
        return lines_by_drama

    def get_lines_for_drama(self, drama):
        if not JdsDatabase.__check_state():
            return
        sql = "SELECT * FROM line WHERE drama_uid={}".format(drama.uid)
        results = self.__cursor_execute_fetchall_thread_safe(sql)
        lines = []
        try:
            for result in results:
                lines.append(JdsLine(result['line_uid'], result['drama_uid'], result['value']))
        except Exception as e:
            exception(e)
        return lines

    def get_all_chars_with_count(self):
        if not JdsDatabase.__check_state():
            return
        sql = """ SELECT a.value, a.kanji_uid, b.count
                    FROM kanji a
                    INNER JOIN count b
                    ON a.kanji_uid = b.kanji_uid
                    WHERE b.drama_uid = 0
                """
        results = self.__cursor_execute_fetchall_thread_safe(sql)
        chars = {}
        try:
            for result in results:
                c = JdsChar(chr(result['kanji_uid']))
                c.set_count(result['count'])
                chars[result['kanji_uid']] = c
        except Exception as e:
            exception(e)
        return chars

    def get_all_chars(self):
        if not JdsDatabase.__check_state():
            return
        sql = "SELECT * FROM kanji "
        results = self.__cursor_execute_fetchall_thread_safe(sql)
        chars = {}
        try:
            for result in results:
                chars[result['kanji_uid']] = JdsChar(chr(result['kanji_uid']))
        except Exception as e:
            exception(e)
        return chars

    def get_count_for_drama(self, drama):
        if not JdsDatabase.__check_state():
            return
        sql = "SELECT * FROM count WHERE drama_uid={} ".format(drama.uid)
        results = self.__cursor_execute_fetchall_thread_safe(sql)
        res = {}
        try:
            for result in results:
                res[result['kanji_uid']] = result['count']
        except Exception as e:
            exception(e)
        return res

    def push_lines(self, lines):
        if not self.__check_state():
            return

        sql_inserts = []
        packet_size = 0
        for line in lines:
            line_value = self.__escape_sql(line.value)
            sql_insert = "({},{},'{}')".format(line.uid, line.drama_uid, line_value)

            # push if we will reach max_allowed_packets
            if (packet_size + len(sql_insert)) >= self.max_allowed_packets / 2:
                sql = "INSERT INTO line (line_uid, drama_uid, value) VALUES {}".format(",".join(sql_inserts))
                self.__cursor_execute_thread_safe(sql)
                sql_inserts.clear()
                packet_size = 0

            packet_size += len(sql_insert)
            sql_inserts.append(sql_insert)

        # push the remaining part
        if len(sql_inserts) > 0:
            sql = "INSERT INTO line (line_uid, drama_uid, value) VALUES {}".format(",".join(sql_inserts))
            self.__cursor_execute_thread_safe(sql)

    def push_dramas(self, dramas):
        if not self.__check_state():
            return
        sql_inserts = []
        for drama in dramas:
            drama_value = self.__escape_sql(drama.value)
            sql_insert = "({},'{}')".format(drama.uid, drama_value)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO drama (drama_uid, name) VALUES {}".format(",".join(sql_inserts))
        self.__cursor_execute_thread_safe(sql)

    def push_chars_to_line(self, chars):
        if len(chars) is 0:
            return
        sql_inserts = []
        for char_uid, char in chars.items():
            count = 0
            for line_uid in char.lines:
                sql_insert = "({},{})".format(char.uid, line_uid)
                sql_inserts.append(sql_insert)
                count += 1
                if count == 10:
                    break
        if len(sql_inserts) is 0:
            return
        sql = "INSERT INTO kanji_to_line (kanji_uid, line_uid) VALUES {}".format(",".join(sql_inserts))
        self.__cursor_execute_thread_safe(sql)
        sql_inserts.clear()

        sql = "INSERT INTO drama (drama_uid, kanji_line_ref_ok) VALUES ({},{}) ON DUPLICATE KEY UPDATE drama_uid=VALUES(drama_uid), kanji_line_ref_ok=VALUES(kanji_line_ref_ok)".format(char.drama_uid, True)
        self.__cursor_execute_thread_safe(sql)

    def push_chars_count(self, chars):
        if len(chars) is 0:
            return
        sql_inserts = []
        for char_uid, char in chars.items():
            sql_insert = "({},{},{})".format(char.uid, char.drama_uid, char.count())
            sql_inserts.append(sql_insert)

        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
        self.__cursor_execute_thread_safe(sql)
        sql_inserts.clear()

        sql = "INSERT INTO drama (drama_uid, kanji_ok) VALUES ({},{}) ON DUPLICATE KEY UPDATE drama_uid=VALUES(drama_uid), kanji_ok=VALUES(kanji_ok)".format(char.drama_uid, True)
        self.__cursor_execute_thread_safe(sql)

    def push_char(self, char):
        # push kanji
        sql = "INSERT INTO kanji (kanji_uid, value) VALUES ({},'{}')".format(char.uid, self.__escape_sql(char.value))
        self.__cursor_execute_thread_safe(sql)

        # push  total count
        drama_id = char.drama_uid
        if drama_id is None:
            drama_id = 0
        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES ({},{},{})".format(char.uid, drama_id, char.count())
        self.__cursor_execute_thread_safe(sql)

    def push_chars(self):

        # delete total count
        sql = "DELETE FROM count WHERE drama_uid=0"
        self.__cursor_execute_thread_safe(sql)

        # delete kanji
        sql = "DELETE FROM kanji"
        self.__cursor_execute_thread_safe(sql)

        sql = "SELECT * FROM count"
        results = self.__cursor_execute_fetchall_thread_safe(sql)

        # sum everything
        chars = {}
        counts = {}
        for result in results:
            kanji_uid = result["kanji_uid"]
            count = result["count"]
            if kanji_uid not in chars:
                chars[kanji_uid] = JdsChar(chr(kanji_uid))
                counts[kanji_uid] = 0
            counts[kanji_uid] += count

        # push kanji
        sql_inserts = []
        for char in chars.values():
            sql_insert = "({},'{}')".format(char.uid, self.__escape_sql(char.value))
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO kanji (kanji_uid, value) VALUES {}".format(",".join(sql_inserts))
        self.__cursor_execute_thread_safe(sql)

        # push total count
        sql_inserts = []
        for uid, count in counts.items():
            sql_insert = "({},{},{})".format(uid, 0, count)
            sql_inserts.append(sql_insert)

        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
        self.__cursor_execute_thread_safe(sql)

    def push_kanji_info_flags(self, chars):
        sql_inserts = []
        for char in chars.values():
            sql_insert = "({},{})".format(char.uid, char.flag)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO kanji_info (kanji_uid, flag) VALUES {} ON DUPLICATE KEY UPDATE kanji_uid=VALUES(kanji_uid), flag=VALUES(flag)".format(",".join(sql_inserts))
        print(sql)
        self.__cursor_execute_thread_safe(sql)

    def push_kanji_jlpt_joyo(self, chars):
        sql_inserts = []
        for char in chars.values():
            sql_insert = "({},{},{})".format(char.uid, char.jlpt, char.jouyou)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO kanji_info (kanji_uid, jlpt, jouyou) VALUES {} ON DUPLICATE KEY UPDATE kanji_uid=VALUES(kanji_uid), jlpt=VALUES(jlpt), jouyou=VALUES(jouyou)".format(",".join(sql_inserts))
        print(sql)
        self.__cursor_execute_thread_safe(sql)

    def push_kanji_pos(self, chars):
        sql_inserts = []
        for char in chars.values():
            sql_insert = "({},{},{},{},{},{},{},{})".format(char.uid, char.jlpt_pos, char.jouyou_pos, char.jdpt_pos, char.jdpt, char.jdpt_to_jlpt(), char.freq, char.freq_cum)
            sql_inserts.append(sql_insert)

        sql = "INSERT INTO kanji_info (kanji_uid, jlpt_pos, jouyou_pos, jdpt_pos, jdpt, jdpt_to_jlpt, freq, freq_cum) VALUES {} ON DUPLICATE KEY UPDATE kanji_uid=VALUES(kanji_uid), jlpt_pos=VALUES(jlpt_pos), jouyou_pos=VALUES(jouyou_pos), jdpt_pos=VALUES(jdpt_pos), jdpt=VALUES(jdpt), jdpt_to_jlpt=VALUES(jdpt_to_jlpt), freq=VALUES(freq), freq_cum=VALUES(freq_cum)".format(",".join(sql_inserts))
        print(sql)
        self.__cursor_execute_thread_safe(sql)

    def prepare_info(self, chars):
        # prepare info table
        sql_inserts = []
        for char in chars.values():
            sql_insert = "({})".format(char.uid)
            sql_inserts.append(sql_insert)

        sql = "INSERT INTO kanji_info (kanji_uid) VALUES {}".format(",".join(sql_inserts))
        self.__cursor_execute_thread_safe(sql)

    def reset_lines(self):
        if not self.__check_state():
            return

        print("Dropping table 'line'")
        sql = "DROP TABLE IF EXISTS line"
        self.__cursor.execute(sql)

        print("Creating table 'line'")
        sql = "CREATE TABLE line (line_uid INT UNSIGNED PRIMARY KEY NOT NULL, drama_uid SMALLINT NOT NULL, value TEXT, INDEX(line_uid), INDEX(drama_uid))"
        self.__cursor.execute(sql)

    def reset_dramas(self):
        if not self.__check_state():
            return
        print("Dropping table 'drama'")
        sql = "DROP TABLE IF EXISTS drama"
        self.__cursor.execute(sql)

        print("Creating table 'drama'")
        sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255), kanji_ok TINYINT,word_ok TINYINT, kanji_line_ref_ok TINYINT,word_line_ref_ok TINYINT, INDEX(drama_uid))"
        self.__cursor.execute(sql)

    def reset_chars(self):
        if not self.__check_state():
            return
        print("Dropping chars table ")

        sql = "DROP TABLE IF EXISTS count"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji_flag"
        self.__cursor.execute(sql)

        print("Creating chars table")

        self.create_char_tables()

        self.reset_kanji_ok_for_all_drama()

        self.reset_info()

    def reset_info(self):
        if not self.__check_state():
            return
        sql = "DROP TABLE IF EXISTS kanji_info"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS word_info"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE kanji_info (kanji_uid INT UNSIGNED PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT, jdpt TINYINT, jlpt_pos  SMALLINT UNSIGNED, jouyou_pos  SMALLINT UNSIGNED, jdpt_pos SMALLINT UNSIGNED, jdpt_to_jlpt SMALLINT , flag TINYINT,freq FLOAT, freq_cum FLOAT, INDEX(kanji_uid,jlpt, jouyou, jdpt, jlpt_pos, jouyou_pos,jdpt_pos, flag))"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE word_info (word_uid INT UNSIGNED PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT, jdpt TINYINT, jlpt_pos SMALLINT UNSIGNED, jouyou_pos  SMALLINT  UNSIGNED, jdpt_pos   SMALLINT UNSIGNED, flag TINYINT, freq FLOAT, freq_cum FLOAT,INDEX(word_uid,jlpt, jouyou, jdpt, jlpt_pos, jouyou_pos,jdpt_pos, flag))"
        self.__cursor.execute(sql)

    def reset_kanji_ok_for_all_drama(self):
        if not self.__check_state():
            return
        sql = "UPDATE drama SET kanji_ok=0".format(0)
        self.__cursor_execute_thread_safe(sql)

    def create_char_tables(self):
        if not self.__check_state():
            return
        sql = "CREATE TABLE IF NOT EXISTS  count (kanji_uid INT UNSIGNED, drama_uid SMALLINT , count INT UNSIGNED, INDEX(kanji_uid), INDEX(drama_uid))"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS kanji (kanji_uid INT UNSIGNED PRIMARY KEY NOT NULL, value VARCHAR(1))"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji_flag"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS kanji_flag (id SMALLINT PRIMARY KEY NOT NULL, value VARCHAR(255), INDEX(id,value))"
        self.__cursor.execute(sql)

        sql = "INSERT INTO kanji_flag (id, value) VALUES (1,'Kana'),(2,'Kanji'),(3,'Unreadable')"
        self.__cursor.execute(sql)

    def reset_line_refs(self):
        if not self.__check_state():
            return
        sql = "DROP TABLE IF EXISTS kanji_to_line"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS kanji_to_line (kanji_uid INT UNSIGNED, line_uid INT UNSIGNED , INDEX(kanji_uid), INDEX(line_uid)) "
        self.__cursor.execute(sql)

        sql = "UPDATE drama SET kanji_line_ref_ok=0".format(0)
        self.__cursor_execute_thread_safe(sql)
