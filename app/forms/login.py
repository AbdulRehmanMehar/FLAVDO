from wtforms import Form, StringField, PasswordField, validators, ValidationError
from ..models import User

class LoginForm(Form):
    username = StringField('Username or Email', [
        validators.DataRequired()
    ], description='jone')
    
    def validate_username(self, field):
        self.user = User.query.filter((User.email == field.data) | (User.username == field.data)).first()
        if self.user == None:
            raise ValidationError('Username or Email was not found in record.')
    
    password = PasswordField('Password', [
        validators.DataRequired()
    ], description='**********')

    def validate_password(self, field):
        if self.user == None or not self.user.compare(field.data):
            raise ValidationError('Incorrect Credentials were provided.')
