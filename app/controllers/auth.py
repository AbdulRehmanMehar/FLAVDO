from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import app, mail
from ..models import db, User
from ..forms import LoginForm, RegisterationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm(request.form)
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard.home'))
    if request.method == 'POST' and form.validate():
        login_user(form.get_user())
        flash('You\'re logged in successfully.', 'success')
        return redirect(url_for('dashboard.home'))
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard.home'))
    form = RegisterationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data, form.username.data, form.password.data)
        mail.send_email(
            to_email=[{'email': user.email}],
            subject='Authentication',
            html='<h1>Hey ' + user.name + '</h1><p>Please verify your email (' + user.email + ') by clicking <a href="'+ app.config['APP_URI'] +'/auth/'+ user.get_id() +'/'+ user.verificationToken +'">here</a>.</p>'
        )
        db.session.add(user)
        db.session.commit()
        flash('Your email is now registered with ' + app.config['APP_NAME'] + '.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('<id>/<token>')
def verify(id, token):
    user = User.query.filter(User.id == id and User.verificationToken==token and User.verified==False).first()
    if(user == None):
        flash('Sorry, something went wrong.', 'danger')
        return redirect(url_for('auth.register'))
    else:
        user.verified = True
        user.verificationToken = None
        db.session.commit()
        flash('Your email is now verified.', 'success')
        return redirect(url_for('auth.login'))
