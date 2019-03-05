import os, binascii
from flask_login import UserMixin
from passlib.hash import sha256_crypt
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
    verificationToken = db.Column('verificationToken', db.String, nullable=True)

    def __init__(self, name, email, username, password, admin=False, verified=False):
        self.name = name
        self.email = email
        self.username = username
        self.password = sha256_crypt.encrypt(password)
        self.admin = admin
        self.verified = verified
        user = User.query.order_by(User.id.desc()).first()
        if(user == None):
            self.id = 1
        else:
            self.id = user.id + 1
        if(not verified):
            self.verificationToken = self.set_token()
        else:
            self.verificationToken = None

    def compare(self, pwd):
        return sha256_crypt.verify(pwd, self.password)

    def set_token(self):
        return str(binascii.b2a_hex(os.urandom(15)))

    def __repr__(self):
        return '<User %r>' % self.username
