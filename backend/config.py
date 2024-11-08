import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_DATABASE = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALQUEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///Quickr.db')


class ProductionConfig(Config):
    DEBUG = False
    SQLALQUEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///Quickr.db')
