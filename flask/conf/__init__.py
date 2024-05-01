class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

from .test import TestConfig
from .prod import ProductionConfig

