# basic
import os

# flask modules
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_continuum import make_versioned
import conf


app = Flask(__name__)
api = Api(app)

if ( os.environ.get("FLASK_ENV") == "testing" ):
    app.config.from_object(conf.TestConfig) 
elif ( os.environ.get("FLASK_ENV") == "production" ):
    app.config.from_object(conf.ProductionConfig)

db = SQLAlchemy(app)
make_versioned

from urls import loadUrls
loadUrls(api)

## INIT
if __name__ == "__main__":
    app.run()
