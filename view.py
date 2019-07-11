import models
from models import User, Tokens
from flask.views import MethodView
from app import app, db, bcrypt
from flask import request, make_response, jsonify


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
            make_response(jsonify(response_obj), 200)


class Logout(MethodView):

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ""
        if token:
            check_token = Tokens.query.filter_by(token=token).first()
            if check_token:
                db.session.delete(check_token)
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
        else:
            response_obj = {
                'message': 'Invalid token'
            }
            return make_response(jsonify(response_obj), 403)


class UserHistory(MethodView):

    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ""
        if token:
            curr = Tokens.query.filter_by(token=token).first()
        else:
            return 'Access is forbidden', 403
        if curr:
            history = curr.history

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ""
        if token:
            curr = Tokens.query.filter_by(token=token).first()
        else:
            return 'Access is forbidden', 403


app.add_url_rule('/register/', view_func=Register.as_view('register'))
app.add_url_rule('/auth/', view_func=Auth.as_view('auth'))
app.add_url_rule('/logout/', view_func=Logout.as_view('logout'))
app.add_url_rule('/history/', view_func=UserHistory.as_view('user_history'))
