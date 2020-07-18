import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    S3_BUCKET_NAME = getenv('S3_BUCKET_NAME')
    S3_ACCESS_KEY = getenv('S3_ACCESS_KEY')
    S3_SECRET_ACCESS_KEY = getenv('S3_SECRET_ACCESS_KEY')
    S3_BASE_URL = getenv('S3_BASE_URL')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    SENTRY_DSN_KEY = getenv('SENTRY_DSN_KEY')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URL')
