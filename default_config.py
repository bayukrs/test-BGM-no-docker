import os

DEBUG = True
ENV = "develpoment"
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URI", "sqlite:///user.db"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
SECRET_KET = os.environ['APP_SECRET_KEY']
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
