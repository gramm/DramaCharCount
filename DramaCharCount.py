import sys, getopt
import mysql.connector
from mysql.connector import Error

sql_host = "",
sql_user = "",
sql_password = ""
sql_database = ""


def parse_args(argv):
    """
    Parse the arguments for MySql connection
    :param argv:
    :return:
    """
    global sql_host, sql_password, sql_user, sql_database
    try:
        opts, args = getopt.getopt(argv, "h:u:p:db", ["host=", "user=", "password=", "database="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print("Could not parse program arguments")
        print(str(err))  # will print something like "option -a not recognized"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--host'):
            sql_host = arg
            print("sql_host = {}".format(sql_host))
        elif opt in ('-u', '--user'):
            sql_user = arg
            print("sql_user = {}".format(sql_user))
        elif opt in ('-p', '--password'):
            sql_password = arg
            print("sql_password = {}".format(sql_password))
        elif opt in ('-db', '--database'):
            sql_database = arg
            print("sql_database = {}".format(sql_database))
        else:
            sys.exit(2)
    if not sql_host or not sql_password or not sql_user or not sql_database:
        print("Missing command line arguments")
        sys.exit(2)


def main(argv):
    global sql_host, sql_password, sql_user, sql_database
    parse_args(argv)

    try:
        mydb = mysql.connector.connect(
            host=sql_host,
            database=sql_database,
            user=sql_user,
            password=sql_password,
        )
    except Error as e:
        print("Error while connecting to MySQL", e)

    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Could not connect to database, exiting...")
        sys.exit(2)
    

if __name__ == "__main__":
    print("DramaCharCount started")
    main(sys.argv[1:])
    print("DramaCharCount successfully executed")
