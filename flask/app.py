# flask modules
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_continuum import make_versioned

## method to generate connection uri
def get_uri(env):
    if env=="DEV":
        return 'sqlite:///test.db'
    elif env=="PROD":
        ## Read secrets
        DB_HOST="mysql"
        DB_NAME="nawas"
        DB_USER="api"
        DB_PASSWORD_FILE="/run/secrets/db_password"
        DB_PASSWORD = None
    
        with open(DB_PASSWORD_FILE) as f:
            DB_PASSWORD = f.readlines()
    
        if DB_PASSWORD is None:
            raise DBPasswordNotFoundException("db_password was not found in the expected location (/run/secrets/db_password)")
    
        return "mysql+mysqlconnector://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)

## custom error for missing password in secrets location
class DBPasswordNotFoundException(Exception):
    def __init__(self, message, errors=401):
        super().__init__(message)
        self.errors = errors

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = get_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
make_versioned

db = SQLAlchemy(app)

from urls import initUrls
initUrls(api)

## INIT
if __name__ == "__main__":
    app.config["DEBUG"] = bool(os.environ.get("DEBUG"))
    app.config["RESTFUL_JSON"] = {
        "ensure_ascii": False
    }
    app.run(host = "0.0.0.0")
