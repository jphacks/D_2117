import flask_wtf
from wtforms import SubmitField, validators, FileField, TextAreaField, SelectField


class ThreadForm(flask_wtf.FlaskForm):

    message = TextAreaField(
        'message',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 200, "最大200文字")],
    )

    img = FileField('img')

    pet_id = SelectField('pet_id', [validators.DataRequired(
        "先にペット名を登録してください。")], choices=[])  # ペットの名前選択

    sub = SubmitField("登録")
