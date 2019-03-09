import re
from . import app
from wtforms import Form, FileField, ValidationError, validators

class VideoUploadForm(Form):
    video = FileField('Add video', [
        validators.DataRequired(message='Video is required.')
    ], description='Choose a video')

    def validate_video(self, field):
        self.ext = field.data.filename.split('.').pop()
        if not self.ext in app.config['UPLOAD_ABLE_VIDEOS']:
            raise ValidationError('Invalid file has been selected.')
