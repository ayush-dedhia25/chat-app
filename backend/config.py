import os


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
