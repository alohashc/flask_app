from app import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    pw_hash = db.Column(db.String(180), unique=True)

    def __init__(self, login, password):
        self.login = login
        self.pw_hash = bcrypt.generate_password_hash(password).decode('utf8')


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


db.create_all()
