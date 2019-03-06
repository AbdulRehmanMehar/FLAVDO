import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from flask_login import login_user, login_required, logout_user, current_user
from . import app, mail
from ..models import db, User
from ..forms import LoginForm, RegisterationForm, PhotoUploadForm

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

@auth.route('/send-token')
@login_required
def send_token():
    user = User.query.filter(User.id == current_user.id).first()
    user.verificationToken = user.set_token()
    mail.send_email(
        to_email=[{'email': user.email}],
        subject='Authentication',
        html='<h1>Hey ' + user.name + '</h1><p>Please verify your email (' + user.email + ') by clicking <a href="' + app.config['APP_URI'] + '/auth/' + user.get_id() + '/' +user.verificationToken + '">here</a>.</p>'
    )
    db.session.commit()
    flash('Verification email sent.', 'success')
    # if something wents wrong, it will redirect to login instead of dashboard
    redir = request.args.get('next') or request.referrer or url_for('auth.login')
    return redirect(redir)

@auth.route('/upload-photo', methods=['GET', 'POST'])
@login_required
def upload_photo():
    form = PhotoUploadForm(request.files)
    if request.method == 'POST' and form.validate():
        user = User.query.get(current_user.get_id())
        if user.photo != None:
            os.remove(os.path.join(app.config['UPLOADS_FOLDER'] + '/images', user.photo))
        photo = request.files[form.photo.name]
        filename = current_user.username + '.' + form.ext
        photo.save(os.path.join(app.config['UPLOADS_FOLDER'] + '/images', filename))
        user.photo = filename
        db.session.commit()
        flash('Photo has been uploaded.', 'success')
        redir = request.args.get('next') or request.referrer or url_for('auth.login')
        return redirect(redir)

    return render_template('photo-upload.html', form=form)


@auth.route('/remove-photo', methods=['GET'])
@login_required
def remove_photo():
    user = User.query.get(current_user.get_id())
    if user.photo != None:
        os.remove(os.path.join(app.config['UPLOADS_FOLDER'] + '/images', user.photo))
        user.photo = None
        db.session.commit()
        flash('Photo has been removed', 'success')
    redir = request.args.get('next') or request.referrer or url_for('auth.login')
    return redirect(redir)

@auth.route('/get-photo/<uname>')
def get_photo(uname):
    user = User.query.filter(User.username == uname).first()
    if user != None:
        path = os.path.join(app.config['UPLOADS_FOLDER'] + '/images', user.photo)
        return send_file(path)
    return send_file(os.path.join(app.config['UPLOADS_FOLDER'] + '/images', 'default.jpg'))

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
