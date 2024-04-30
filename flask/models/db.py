
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_continuum import make_versioned

class DBConnection:
    connection = None

    def init(app):
        app.config['SQLALCHEMY_DATABASE_URI'] = DBConnection.build_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        make_versioned

        connection = SQLAlchemy(app)

    def build_uri():
        ## Read secrets
        DB_HOST="mysql"
        DB_NAME="nawas"
        DB_USER="api"
        DB_PASSWORD_FILE="/run/secrets/DB_PASSWORD"
        DB_PASSWORD = None

        with open(DB_PASSWORD_FILE) as f:
            DB_PASSWORD = f.readlines()

        if DB_PASSWORD is None:
            raise DBPasswordNotFoundException("DB_PASSWORD was not found in the expected location (/run/secrets/DB_PASSWORD)")

        return "mysql://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)


    def get_connection():
        if connection is None:
            raise DBConnectionNotInitialisedException("DBConnection was not initialised before requesting connection")

        return connection


## custom error for missing password in secrets location
class DBPasswordNotFoundException(Exception):
    def __init__(self, message, errors):
        super().init(message)

## custom error for when connection is requested before DBConnection has run init(app)
class DBConnectionNotInitialisedException(Exception):
    def __init__(self, message, errors):
        super().init(message)
