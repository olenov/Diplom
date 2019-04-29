import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration():
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgres://sql:1@localhost/Student')