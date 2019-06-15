import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration():

    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgres://sql:1@localhost/Students2' # 'postgres://sql:1@localhost/Student'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    WHOOSH_BASE = 'whoosh'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'olenov1994@gmail.com'
    MAIL_PASSWORD = 'soslow1994'

