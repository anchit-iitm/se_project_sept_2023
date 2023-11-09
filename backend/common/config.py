import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDev(Config):
    # database configurations
    SQLITE_DB_DIR = os.path.join(basedir, '../db_raw')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'db.sqlite3')
    
    # security configurations
    SECRET_KEY = "TEMPORARY_KEY_FOR_DEV" #os.environ.get('FLASK_SECRET')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = "TEMPORARY_KEY_FOR_DEV" #os.environ.get('SECURITY_SECRET')
    SECURITY_REGISTERABLE = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = "TEMPORARY_KEY_FOR_DEV" #os.environ.get('SECURITY_SECRET')
    WTF_CSRF_ENABLED = False
    JSON_SORT_KEYS = False

    # debug application
    DEBUG = True

class ProductionDev(Config):
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'prod_db.sqlite3')
    DEBUG = False