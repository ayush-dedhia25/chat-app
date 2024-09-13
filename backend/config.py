import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
