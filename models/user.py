from typing import List

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    referral_code = db.Column(db.String)

    @classmethod
    def find_by_id(cls, _id: str) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_name(cls, name: str) -> List["UserModel"]:
        return cls.query.filter_by(name=name)

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_ref(cls, ref: str) -> "UserModel":
        return cls.query.filter_by(referral_code=ref).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
