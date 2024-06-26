# basic
import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## load urls from the urls file, using this method to prevent premature loading of the models
def load_urls(app, api):
    from app.urls import loadUrls
    app.logger.debug("loading URLs")
    loadUrls(api)

## initialize database and create all tables if necessary
def init_db(app):
    app.logger.debug("Initialising database integration")
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        app.logger.debug("Tables have been created")

## start the app and initialize database and urls
#             test       Boolean      starts the application using test configuration (with a sqlite database in memory)
#
# @returns    app        Object       object containing the flask application
def create_app(test=False):
    app = Flask(__name__)
    app.logger.debug("Starting application")
    api = Api(app)
    app.logger.debug("Adding api function")
    
    app.logger.debug("Loading config")
    if ( test ):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.logger.debug("loaded testing config...")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = get_prod_uri()
        app.logger.debug("loaded config...")
    
    load_urls(app, api)
    init_db(app)

    return app

## production configuration
#  @throws  DBPasswordNotFoundException if the database password is not present in /run/secrets
#  @returns connection string for mysql database
def get_prod_uri():
    ## Read secrets
    DB_HOST="db"
    DB_NAME="nawas"
    DB_USER="api"
    DB_PASSWORD_FILE="/run/secrets/db_password"
    DB_PASSWORD = None

    with open(DB_PASSWORD_FILE) as f:
        DB_PASSWORD = f.read().replace('\n', '')

    if DB_PASSWORD is None:
        raise DBPasswordNotFoundException("db_password was not found in the expected location (/run/secrets/db_password)")

    return "mysql+mysqlconnector://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)
    
## custom error for missing password in secrets location
class DBPasswordNotFoundException(Exception):
    def __init__(self, message, errors=401):
        super().__init__(message)
        self.errors = errors



