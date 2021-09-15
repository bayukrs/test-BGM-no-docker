import re
from hashlib import md5
from uuid import uuid4

import requests
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from schema.user import UserSchema

user_schema = UserSchema()
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

def checkemail(email):
    if (re.fullmatch(regex, email)):
        return True
    return False


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = user_schema.load(data)
        if UserModel.find_by_username(user.username):
            return {"message": "Username already exists"}, 400
        if UserModel.find_by_email(user.email):
            return {"message": "Email already exitsts"}, 400
        if not checkemail(user.email):
            return {"message": "This email <{}> is not valid".format(user.email)}, 400
        user.password = md5(user.password.encode('utf-8')).hexdigest()
        user.referral_code = uuid4().hex
        try:
            user.save_to_db()
        except:
            return {"message": "Invalid credential error"}, 500
        return user_schema.dump(user), 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = UserModel.find_by_username(data["username"])
        if not user:
            return {"message": "Username/password is wrong"}, 400
        password = md5(data['password'].encode('utf-8')).hexdigest()
        if user and user.password and safe_str_cmp(user.password, password):
            access_token = create_access_token(
                identity=user.id, fresh=True
            )
            return {"user": user_schema.dump(user), "token": access_token}
        return {"message": "Username/password is wrong"}, 400


class UserUpdate(Resource):
    @classmethod
    @jwt_required()
    def put(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        data = request.get_json()
        if not checkemail(data['email']):
            return {"message": "This email <{}> is not valid".format(user.email)}, 400
        for key, value in data.items():
            setattr(user, key, value)
        try:
            user.save_to_db()
        except:
            return {"message": "Invalid credential error"}, 500
        return user_schema.dump(user)


class UserInputRef(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        data = request.get_json()
        if data['referral_code'] == user.referral_code:
            return {"message": "You cannot user your own referral_code"}, 400
        if not UserModel.find_by_ref(data['referral_code']):
            return {"message": "Refferal Code not found"}, 404
        return {"message": "OK"}, 200


class UserByName(Resource):
    @classmethod
    def get(cls):
        data = request.get_json()
        return user_schema.dump(UserModel.find_by_name(data['name']), many=True)


class GetHero(Resource):
    @classmethod
    def get(cls):
        data = requests.get(url="https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json").json()
        input_hero = request.get_json()
        if data['data'][input_hero['name']]:
            return data['data'][input_hero['name']], 200
        return {"message": "Hero name not found"}, 404
