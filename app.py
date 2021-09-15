import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

from resource.user import UserRegister, UserLogin, UserByName, UserUpdate, UserInputRef, GetHero

load_dotenv('.env', verbose=True)
from db import db
from ma import ma

app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)

migrate = Migrate(app, db)

@app.before_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserUpdate, "/user/update")
api.add_resource(UserInputRef, "/user/referral_code")
api.add_resource(UserByName, "/user/search")
api.add_resource(GetHero, "/search/hero")

if __name__ == "__main__":
    ma.init_app(app)
    app.run(port=5000)
