from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), nullable=False)
    email = db.Column('email',db.String(120), unique=True, nullable=False)
    username = db.Column('username', db.String(80), unique=True, nullable=False)
    password = db.Column('password', db.String(200), nullable=False)
    admin = db.Column('admin', db.Boolean, nullable=False, default=False)
    verified = db.Column('verified', db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, username, password, admin=False, verified=False):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.admin = admin
        self.verified = verified
        user = User.query.order_by(User.id.desc()).first()
        if(user == None):
            self.id = 1
        else:
            self.id = user.id + 1

    def __repr__(self):
        return '<User %r>' % self.username
