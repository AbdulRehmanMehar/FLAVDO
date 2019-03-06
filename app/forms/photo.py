import re
from . import app
from wtforms import Form, FileField, TextField, ValidationError, validators

class PhotoUploadForm(Form):
    photo = FileField('Profile Picture', [
        validators.DataRequired(message='Image is required.')
    ], description='Choose a photo')

    def validate_photo(self, field):
        self.ext = field.data.filename.split('.').pop()
        if not self.ext in app.config['UPLOAD_ABLE_IMAGES']:
            raise ValidationError('Invalid file has been selected.')
