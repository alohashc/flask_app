from flask.views import MethodView
from app import app
from flask import request


class Registration(MethodView):

    def post(self):
        data = request.form


class Auth(MethodView):

    def post(self):
        pass


class Logout(MethodView):

    def post(self):
        pass


class UserHistory(MethodView):

    def get(self):
        pass

    def post(self):
        pass


app.add_url_rule('/registration/', view_func=Registration.as_view('registration'))
app.add_url_rule('/auth', view_func=Auth.as_view('auth'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/history', view_func=UserHistory.as_view('user_history'))
