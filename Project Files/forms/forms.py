from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class UploadForm(FlaskForm):
    image = FileField('Upload Rice Grain Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Classify')