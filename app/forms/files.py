from flask_wtf import FlaskForm
from wtforms.fields import SubmitField

from flask_wtf.file import FileField

from app.data.texts import texts


class PhotoForm(FlaskForm):
    file = FileField("Fotka")
    submit = SubmitField(texts.image.upload)
