import mysql
from mysql.connector import Error

from python.JdsDrama import JdsDrama


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
                connection_timeout=connection_timeout
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

        if JdsDatabase.__db.is_connected():
            print("Database connection successful")
            JdsDatabase.__cursor = JdsDatabase.__db.cursor()
            return True
        else:
            print("Could not connect to database")
            return False

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
            return JdsDrama(result[0], result[1])  # fixme: better way to access columns
        else:
            return None
