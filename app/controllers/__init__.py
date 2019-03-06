from .. import app, mail
from flask_login import current_user
from flask import Blueprint, render_template

index = Blueprint('app', __name__)

@index.route('/')
def home():
    return render_template('index.html')
    


# IMPORT other controllers
from .auth import auth
from .dashboard import dashboard

# REGISTER CONTROLLERS
app.register_blueprint(index)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dashboard, url_prefix='/dashboard')
