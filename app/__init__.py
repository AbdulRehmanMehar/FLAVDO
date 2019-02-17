import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# INITIALIZE APPLICATION

app = Flask(__name__)

app.template_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'views')

app.static_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'public')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/videoserver'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# IMPORT SUB MODULES
from .controllers import *
