import os
from cv2 import cv2 
from .. import app, mail
from flask_login import current_user
from flask import Blueprint, render_template, send_file
from ..models import Video

index = Blueprint('app', __name__)

@index.route('/')
def home():
    return render_template('index.html')
    
@index.route('/get-video/<id>')
def get_video(id):
    video = Video.query.get(id)
    path = os.path.join(app.config['UPLOADS_FOLDER'] + '/videos', video.filename)
    return send_file(path)

# IMPORT other controllers
from .auth import auth
from .dashboard import dashboard

# REGISTER CONTROLLERS
app.register_blueprint(index)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dashboard, url_prefix='/dashboard')
