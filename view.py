from models import User, Tokens
from flask.views import MethodView
from app import app, db, bcrypt
from flask import request, make_response, jsonify
from functools import wraps

from datetime import time, datetime, timedelta
from uz_sdk import TicketFinder, BookingSession


def valid_token(token):
    if token:
        return Tokens.query.filter_by(token=token).first()
    else:
        return 'Access is forbidden', 403


def authorization(func):
    @wraps(func)
    def wrapper():
        auth_header = request.headers.get('Authorization')
        token = ""
        if auth_header:
            token = auth_header.split(" ")[1]
        exist = valid_token(token)
        if exist:
            return func(exist)
        return 'Access is forbidden', 403
    return wrapper


class Register(MethodView):

    def post(self):
        data = request.form
        user = User(data['login'], data['password'])

        if not User.query.filter_by(login=data['login']).first():
            db.session.add(user)
            db.session.commit()
            return 'Registration success', 200
        else:
            return 'User exists'


class Auth(MethodView):

    def post(self):
        data = request.form
        user = User.query.filter_by(login=data['login']).first()
        if bcrypt.check_password_hash(user.pw_hash, data['password']):
            token = user.gen_token()
            if token:
                new_token = Tokens(token)
                db.session.add(new_token)
                db.session.commit()
            response_obj = {
                'auth_token': token
            }
            return make_response(jsonify(response_obj), 200)


class Logout(MethodView):

    @authorization
    def post(self, token):
        if token:
            db.session.delete(token)
            db.session.commit()
            response_obj = {
                'message': 'Logged out'
            }
            return make_response(jsonify(response_obj), 200)
        else:
            response_obj = {
                'message': 'Fail'
            }
            return make_response(jsonify(response_obj), 401)


class UserHistory(MethodView):

    @authorization
    def get(self, token):
        history = token.history
        response_obj = {
            'id': history.id,
            'from': history.src,
            'dest': history.dst,
            'date': history.date,
            'places': history.places_type
        }
        return make_response(jsonify(response_obj), 200)


class Tickets(MethodView):

    def post(self):
        data = request.form
        history = UserHistory(data['from'], data['dest'])
        if history:
            db.session.add(history)
            db.session.commit()
        tf = TicketFinder(
            data['from'],
            data['dest'],
            datetime.now() + timedelta(3),
            time(hour=0, minute=0),
            bs=BookingSession(data['session'])
        )

        tf.basic_filters(allowed_types=('П', 'K'))
        info = tf.find()
        print(info)


app.add_url_rule('/register/', view_func=Register.as_view('register'))
app.add_url_rule('/auth/', view_func=Auth.as_view('auth'))
app.add_url_rule('/logout/', view_func=Logout.as_view('logout'))
app.add_url_rule('/history/', view_func=UserHistory.as_view('user_history'))
app.add_url_rule('/tickets/', view_func=Tickets.as_view('tickets'))
