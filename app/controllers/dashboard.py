from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, Markup
from flask_login import current_user

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
def restrict():
    if(not current_user.is_authenticated):
        return abort(401)
    if(not current_user.verified):
        flash('Please verify your email. '+ Markup('<a class="alert-link" href="'+ url_for('auth.send_token') +'">Resend Verification Token?</a>'), 'info')

@dashboard.route('/')
def home():
    return render_template('dashboard.html')

@dashboard.route('/edit-profile')
def edit_profile():
    return render_template('dashboard.html')
