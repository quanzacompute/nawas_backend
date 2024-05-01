class Config:
    def __init__(self):
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

from .test import TestConfig
from .prod import ProdConfig

