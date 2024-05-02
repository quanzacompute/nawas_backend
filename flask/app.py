# basic
import os

# flask modules
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_continuum import make_versioned
import conf


app = Flask(__name__)
app.logger.debug(os.environ.get("DEBUG"))
app.config['DEBUG'] = True
app.logger.debug("Starting application")
api = Api(app)
app.logger.debug("Adding api function")

app.logger.debug("Loading config")
if ( os.environ.get("FLASK_ENV") == "testing" ):
    app.config.from_object(conf.TestConfig)
    app.logger.debug("loaded testing config...")
elif ( os.environ.get("FLASK_ENV") == "production" ):
    app.config.from_object(conf.ProductionConfig)
    app.logger.debug("loaded production config...")


app.logger.debug("Initialising database integration")

db = SQLAlchemy(app)
make_versioned

from urls import loadUrls
app.logger.debug("loading URLs")
loadUrls(api)

with app.app_context():
    db.create_all()

## INIT
if __name__ == "__main__":
#    app.run(debug=bool(os.environ.get("DEBUG")))
    app.run(debug=True)
