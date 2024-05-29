import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') ## or ''
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

class TestingConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    