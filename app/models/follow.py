from datetime import datetime
from . import db

class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column('id', db.Integer, primary_key=True)
    following_id = db.Column('following_id', db.ForeignKey('users.id'))
    follower_id = db.Column('follower_id', db.ForeignKey('users.id'))
    created_on = db.Column('created_on', db.DateTime, default=datetime.utcnow)
    modified_on = db.Column('modified_on', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
