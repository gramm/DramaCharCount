import mysql
from mysql.connector import Error


class JdsDatabase:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.max_allowed_packets = 1048576  # fixme: get from SQL (SHOW VARIABLES LIKE 'max_allowed_packet')
        pass

    def __check_state(self):
        if not self.db:
            print(__class__.__name__ + " not connected to database")
        return self.db

    @staticmethod
    def __escape_sql(sql):
        chars = ['\\', '\'', '\"']
        for c in chars:
            sql = sql.replace(c, '\\' + c)
        sql = sql.replace("\n", "")
        return sql

    def connect(self, args):
        try:
            host = args["sql_host"]
            database = args["sql_database"]
            user = args["sql_user"]
            password = args["sql_password"]
            connection_timeout = 0.1
            print("Connecting {}:{}:{}".format(host, database, user))
            self.db = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                connection_timeout=connection_timeout
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

        if self.db.is_connected():
            print("Database connection successful")
            self.cursor = self.db.cursor()
            return True
        else:
            print("Could not connect to database")
            return False

    def reset_lines(self):
        if not self.__check_state():
            return

        print("Dropping table 'line'")
        sql = "DROP TABLE IF EXISTS line"
        self.cursor.execute(sql)

        print("Creating table 'line'")
        sql = "CREATE TABLE line (line_uid  INT UNSIGNED PRIMARY KEY NOT NULL, value TEXT)"
        self.cursor.execute(sql)

    def reset_dramas(self):
        print("Dropping table 'drama'")
        sql = "DROP TABLE IF EXISTS drama"
        self.cursor.execute(sql)

        print("Creating table 'drama'")
        sql = "CREATE TABLE drama (drama_uid SMALLINT PRIMARY KEY NOT NULL, name VARCHAR(255))"
        self.cursor.execute(sql)

    def push_lines(self, lines):
        if not self.__check_state():
            return

        sql_inserts = []
        packet_size = 0
        for uid, line in lines.items():
            line = self.__escape_sql(line)
            sql_insert = "({},'{}')".format(uid, line)

            # push if we will reach max_allowed_packets
            if (packet_size + len(sql_insert)) > self.max_allowed_packets:
                sql = "INSERT INTO line (line_uid, value) VALUES {}".format(",".join(sql_inserts))
                self.cursor.execute(sql)
                self.db.commit()
                sql_inserts.clear()
                packet_size = 0

            packet_size += len(sql_insert)
            sql_inserts.append(sql_insert)

        # push the remaining part
        if len(sql_inserts) > 0:
            sql = "INSERT INTO line (line_uid, value) VALUES {}".format(",".join(sql_inserts))
            self.cursor.execute(sql)
            self.db.commit()

    def push_dramas(self, dramas):
        sql_inserts = []
        for uid, drama in dramas.items():
            drama = self.__escape_sql(drama)
            sql_insert = "({},'{}')".format(uid, drama)
            sql_inserts.append(sql_insert)
        sql = "INSERT INTO drama (drama_uid, name) VALUES {}".format(",".join(sql_inserts))
        self.cursor.execute(sql)
        self.db.commit()
