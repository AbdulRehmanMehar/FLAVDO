from wtforms import Form, PasswordField, StringField, HiddenField, validators
from flask import Markup

def set_edit_user(user):
    return user

class EditProfileForm(Form):

    name = StringField('Name', [
        validators.DataRequired(),
        validators.Length(min=5, max=25)
    ])

    email = StringField('Email', render_kw={'disabled': True})

    username = StringField('Username', render_kw={'disabled': True})

    password = PasswordField('Password', [
        validators.Optional(),
        validators.Length(min=8, max=25),
        validators.equal_to('cpassword', message='Passwords don\'t match.')
    ], description='************')

    cpassword = PasswordField('Confirm Password', [
        validators.equal_to('password', message='Passwords don\'t match.')
    ], description='************')
