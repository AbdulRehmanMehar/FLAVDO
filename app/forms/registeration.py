from wtforms import Form, PasswordField, StringField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from ..models import User, app

class RegisterationForm(Form):
    name = StringField('Name', [    
        validators.DataRequired(),
        validators.Length(min=5, max=25)
    ], description='Jone Doe')
    email = EmailField('Email Address', [
        validators.DataRequired(), 
        validators.Email()
    ], description='jone@doe.io')

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user != None:
            raise ValidationError('Email already registered.')

    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=10),
        validators.Regexp('(([a-z]+)([^- \[\]A-Z])(([_]+)?)([0-9a-z]?)+)', message='Username may contain lowercase letters, numbers or underscores.Username should begin with lowercase letters.')
    ], description='jone')

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user != None or field in app.config['PROHIBITED_USERNAMES']:
            raise ValidationError('Username not available.')

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=25),
        validators.equal_to('cpassword', message='Passwords don\'t match.')
    ], description='************')  
    cpassword = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.equal_to('password', message='Passwords don\'t match.')
    ], description='************')
