import flask_wtf
from wtforms import StringField, SubmitField, validators, PasswordField


class MemberInfoForm(flask_wtf.FlaskForm):

    user_nickname = StringField(
        'user_nickname',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "最大10文字")],
    )

    user_fname = StringField(
        'user_fname',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "最大10文字")],
    )

    user_lname = StringField(
        'user_lname',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "最大10文字")],
    )

    email = StringField(
        'email',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 50, "最大50文字")],
    )

    password = PasswordField(
        'password',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 50, "最大10文字")],
    )

    password_confirm = PasswordField(
        'password_confirm',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 50, "最大10文字")],
    )

    tell = StringField(
        'tell',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 11, "入力を確認してください(-は入れない)")]
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
    sub = SubmitField("登録")
