import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': os.environ.get('DB_USER'),
    'pw': os.environ.get('DB_PASS'),
    'db': os.environ.get('DB_NAME'),
    'host': os.environ.get('DB_ADDRESS'),
    'port': os.environ.get('DB_PORT'),
}


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class ConfigDevelopment(Config):
    DEBUG = True


class ConfigProduction(Config):
    DEBUG = False