from datetime import datetime
from . import db

class View(db.Model):
    __tablename__ = 'views'

    id = db.Column('id', db.Integer, primary_key=True)
    video_id = db.Column('video_id', db.ForeignKey('videos.id'))
    viewer_id = db.Column('viewer_id', db.ForeignKey('users.id'))
    created_on = db.Column('created_on', db.DateTime, default=datetime.utcnow)
    modified_on = db.Column('modified_on', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
