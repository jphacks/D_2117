import flask_wtf
from wtforms import StringField, SubmitField, validators, IntegerField, FileField, TextAreaField


class PetInfoForm(flask_wtf.FlaskForm):

    pet_name = StringField(
        'pet_name',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 20, "最大20文字")],
    )

    features_description = TextAreaField(
        'features_description',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 200, "最大200文字")],
    )

    img = FileField('img')
    sub = SubmitField("登録")
