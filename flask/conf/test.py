import os
from conf import Config


class TestConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
        self.DEBUG = True
