from datetime import datetime
from . import db

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column('id', db.Integer, primary_key=True)
    video_id = db.Column('video_id', db.ForeignKey('videos.id'))
    liker_id = db.Column('liker_id', db.ForeignKey('users.id'))
    created_on = db.Column('created_on', db.DateTime, default=datetime.utcnow)
    modified_on = db.Column('modified_on', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
