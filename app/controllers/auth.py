from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from . import app, mail
from ..models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'GET':
        return render_template('login.html')
    else:
        return 'POST'

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['c_password']
        mail.send_email(
            to_email=[{'email': 'mehars.6925@gmail.com'}, {'email': email}],
            subject='Authentication',
            text='Hey'
        )
        user = User(name, email, username, password)
        db.session.add(user)
        db.session.commit()
        return username

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
