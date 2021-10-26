import flask_wtf
from wtforms import SubmitField, validators, FileField, TextAreaField, SelectField


class ThreadForm(flask_wtf.FlaskForm):

    message = TextAreaField(
        'message'
    )

    img = FileField('img')

    pet_id = SelectField('pet_id', [], choices=[])  # ペットの名前選択

    sub = SubmitField("登録")
