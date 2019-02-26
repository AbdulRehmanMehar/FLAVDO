from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from . import app, mail
from ..models import db, User
from ..forms import LoginForm, RegisterationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        return form.username.data
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data, form.username.data, form.password.data)
        # mail.send_email(
        #     to_email=[{'email': email}],
        #     subject='Authentication',
        #     html=''
        # )
        db.session.add(user)
        db.session.commit()
        return user.name
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
