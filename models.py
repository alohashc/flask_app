import app
import os
from app import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    pw_hash = db.Column(db.String(180), unique=True)
    history = db.relationship('UserHistory', backref='owner')

    def __init__(self, login, password):
        self.login = login
        self.pw_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def gen_token(self):
        try:
            return os.urandom(24).hex()
        except Exception as e:
            return e


class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    src = db.Column(db.Integer)
    dst = db.Column(db.Integer)
    places_type = db.Column(db.String(2))

    def __init__(self, date=None, src=None, dst=None, places_type=None):
        self.date = date
        self.src = src
        self.dst = dst
        self.places_type = places_type


class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(180), unique=True)
    expired = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, token, expired=False):
        self.token = token
        self.expired = expired


db.create_all()
