import os

basedir = os.path.abspath(os.path.dirname(__file__))

# General Config
SECRET_KEY = 'qwe123'

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'log.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
