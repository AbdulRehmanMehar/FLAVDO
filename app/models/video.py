from datetime import datetime
from . import db, User

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(50), nullable=False)
    description = db.Column('description', db.String(500), nullable=False)
    filename = db.Column('filename', db.String(200), nullable=False, unique=True)
    owner_id = db.Column('owner_id', db.Integer, db.ForeignKey('users.id')) # in foreign key, we provide parent table column
    views = db.relationship('View', backref='video')
    likes = db.relationship('Like', backref='video')
    created_on = db.Column('created_on', db.DateTime, default=datetime.utcnow)
    modified_on = db.Column('modified_on', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title, description, filename, owner_id):
        self.title = title
        self.description = description
        self.filename = filename
        self.owner_id = owner_id

    def __repr__(self):
        return '<Video %r>' % self.title
