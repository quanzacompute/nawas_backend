# basic
import os

# flask modules
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_continuum import make_versioned
import conf

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

db = SQLAlchemy()

if (bool(os.environ.get("TEST"))):
    app.config.from_object(conf.TestConfig())
else:
    app.config.from_object(conf.ProductionConfig())

make_versioned

from urls import initUrls
initUrls(api)

## INIT
if __name__ == "__main__":
    db.init_app(app)
    app.run()
