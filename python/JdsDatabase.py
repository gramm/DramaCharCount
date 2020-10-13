import mysql
from mysql.connector import Error

from python import JdsChar
from python.DccUtils import exception
from python.JdsDrama import JdsDrama
from python.JdsLine import JdsLine


class JdsDatabase:
    __db = None
    __cursor = None

    def __init__(self):
        self.max_allowed_packets = 1048576  # fixme: get from SQL (SHOW VARIABLES LIKE 'max_allowed_packet')
        pass

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
        if args:
            host = args["sql_host"]
            database = args["sql_database"]
            user = args["sql_user"]
            password = args["sql_password"]
        else:
            print("Trying to connect with default parameters")
            host = "localhost"
            database = "db_charcount"
            user = "admin"
            password = "adminpw"
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
            return True
        else:
            print("Could not connect to database")
            return False

    def push_lines(self, lines):
        if not self.__check_state():
            return

        sql_inserts = []
        packet_size = 0
        for line in lines:
            line_value = self.__escape_sql(line.value)
            sql_insert = "({},{},'{}')".format(line.uid, line.drama_uid, line_value)

            # push if we will reach max_allowed_packets
            if (packet_size + len(sql_insert)) > self.max_allowed_packets:
                sql = "INSERT INTO line (line_uid, drama_uid, value) VALUES {}".format(",".join(sql_inserts))
                self.__cursor.execute(sql)
                self.__db.commit()
                sql_inserts.clear()
                packet_size = 0

            packet_size += len(sql_insert)
            sql_inserts.append(sql_insert)

        # push the remaining part
        if len(sql_inserts) > 0:
            sql = "INSERT INTO line (line_uid, drama_uid, value) VALUES {}".format(",".join(sql_inserts))
            self.__cursor.execute(sql)
            self.__db.commit()

    def push_dramas(self, dramas):
        if not self.__check_state():
            return
        sql_inserts = []
        for drama in dramas:
            drama_value = self.__escape_sql(drama.value)
            sql_insert = "({},'{}')".format(drama.uid, drama_value)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO drama (drama_uid, name) VALUES {}".format(",".join(sql_inserts))
        self.__cursor.execute(sql)
        self.__db.commit()

    @staticmethod
    def get_drama(name_or_uid):
        if not JdsDatabase.__check_state():
            return
        if type(name_or_uid) is 'int':
            pass
        else:
            JdsDatabase.__cursor.execute("SELECT * FROM drama WHERE name='{}'".format(JdsDatabase.__escape_sql(name_or_uid)))
            result = JdsDatabase.__cursor.fetchone()

        if result:
            return JdsDrama(result['drama_uid'], result['name'])
        else:
            return None

    def get_all_dramas(self):
        if not JdsDatabase.__check_state():
            return
        self.__cursor.execute("SELECT * FROM drama")
        results = JdsDatabase.__cursor.fetchall()
        dramas = []
        for result in results:
            dramas.append(JdsDrama(result['drama_uid'], result['name']))
        return dramas

    def get_lines_for_drama(self, drama):
        if not JdsDatabase.__check_state():
            return
        self.__cursor.execute("SELECT * FROM line WHERE drama_uid={}".format(drama.uid))
        results = JdsDatabase.__cursor.fetchall()
        lines = []
        try:
            for result in results:
                lines.append(JdsLine(result['line_uid'], result['drama_uid'], result['value'].decode("utf-8")))
        except Exception as e:
            exception(e)
        return lines

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
        sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255), INDEX(drama_uid))"
        self.__cursor.execute(sql)

    def reset_chars(self):
        if not self.__check_state():
            return
        print("Dropping chars table ")

        sql = "DROP TABLE IF EXISTS count"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji_info"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji_flag"
        self.__cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS kanji_to_line"
        self.__cursor.execute(sql)
        print("Creating chars table")

        sql = "CREATE TABLE count (kanji_uid INT UNSIGNED, drama_uid SMALLINT , count INT UNSIGNED, INDEX(kanji_uid), INDEX(drama_uid))"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE kanji (kanji_uid SMALLINT PRIMARY KEY NOT NULL, value NCHAR(1))"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE kanji_info (kanji_uid SMALLINT PRIMARY KEY NOT NULL, jlpt TINYINT, jouyou TINYINT, jdpt TINYINT, dist_to_jlpt TINYINT, dist_to_jdpt TINYINT, flag TINYINT, INDEX(kanji_uid,jlpt, jouyou, jdpt, dist_to_jlpt, dist_to_jdpt,    flag))"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE kanji_flag (id SMALLINT PRIMARY KEY NOT NULL, value VARCHAR(255), INDEX(id,value))"
        self.__cursor.execute(sql)

        sql = "CREATE TABLE kanji_to_line (kanji_uid SMALLINT, line_uid SMALLINT , INDEX(kanji_uid), INDEX(line_uid))"
        self.__cursor.execute(sql)

        sql = "INSERT INTO kanji_flag (id, value) VALUES (1,'Kana'),(2,'Kanji'),(3,'Unreadable')"
        self.__cursor.execute(sql)

    def push_chars(self, chars):
        if len(chars) is 0:
            return
        sql_inserts = []
        for char, count in chars.items():
            sql_insert = "({},{},{})".format(char.uid, char.drama_uid, count)
            sql_inserts.append(sql_insert)

        sql = "INSERT INTO count (kanji_uid, drama_uid, count) VALUES {}".format(",".join(sql_inserts))
        self.__cursor.execute(sql)
