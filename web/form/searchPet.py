import flask_wtf
from wtforms import StringField, SubmitField, validators, IntegerField, FileField, TextAreaField


class SearchPetForm(flask_wtf.FlaskForm):

    features_description = TextAreaField(
        'features_description',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 200, "最大200文字")],
    )

    prefecture = StringField(
        'prefecture',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "最大10文字")],
    )

    city = StringField(
        'city',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 20, "最大20文字")],
    )
    #img = FileField('img', [validators.regexp(u'^[^/\\]\.jpg$')])
    sub = SubmitField("登録")
