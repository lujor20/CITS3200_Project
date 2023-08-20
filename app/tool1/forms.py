from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename

class FileForm(FlaskForm):
  file = FileField(validators=[
    FileRequired(),
    FileAllowed(['docx'])])
    
  submit = SubmitField("Submit File")
