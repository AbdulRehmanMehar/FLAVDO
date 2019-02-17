from .. import app
from flask import Blueprint, render_template

index = Blueprint('controllers', __name__)

@index.route('/')
def home():
    return render_template('index.html')

# IMPORT other controllers
from .auth import router as auth

# REGISTER CONTROLLERS
app.register_blueprint(index)
app.register_blueprint(auth, url_prefix='/auth')
