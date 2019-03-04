from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import current_user

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
def restrict():
    if(not current_user.is_authenticated):
        return abort(401)
    if(not current_user.verified):
        flash('Please verify your email.', 'info')

@dashboard.route('/')
def home():
    return 'Hey'
