from wtforms import Form, StringField, TextAreaField, validators, ValidationError
from ..models import User

class VideoForm(Form):
    title = StringField('Title for video', [
        validators.DataRequired()
    ], description='Lorem ipsum dolor sit amet')

    description = TextAreaField('Description for video', [
        validators.Optional(),
        validators.length(min=50, max=500, message='Minimum 50 and Maximum 500 characters are allowed')
    ], description='Optional, but minimum 50 characters long if provided')
