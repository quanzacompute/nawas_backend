
import os, psycopg2

class DBConnection:
    connection = None
    
    def init_connection():

        ## Read secrets
        DB_HOST="mysql"
        DB_NAME="nawas"
        DB_USER="api"
        DB_PASSWORD_FILE="/run/secrets/DB_PASSWORD"
        DB_PASSWORD = None

        with open(DB_PASSWORD_FILE) as f:
            DB_PASSWORD = f.readlines()

        if DB_PASSWORD is None:
            print("ERROR ERROR NO PASSWORD DETECTED")
            exit(1)

        ## Wait for connection
        while True:
            try:
                connection = psycopg2.connect(
                    "host={} dbname={} user={} password={}".format(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
                )
                break
            except psycopg2.OperationalError:
                sleep(1)
            finally:
                print("DB connection established.")

    def get_connection():
        if connection is None:
            init_connection()

        return connection
    
    def get_cursor():
        get_connection().cursor()

    def close():
        if connection is not None:
            connection.close()
