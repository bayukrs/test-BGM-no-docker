import os

DEBUG = False
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
else:
    uri = os.environ.get("DATABASE_URI")
SQLALCHEMY_DATABASE_URI = uri
