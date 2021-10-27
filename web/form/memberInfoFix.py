import flask_wtf
from wtforms import StringField, SubmitField, validators, PasswordField


class MemberInfoFixForm(flask_wtf.FlaskForm):

    user_nickname = StringField(
        'user_nickname',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "確認してください(最大10文字)")],
    )

    user_fname = StringField(
        'user_fname',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "確認してください(最大10文字)")],
    )

    user_lname = StringField(
        'user_lname',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "確認してください(最大10文字)")],
    )

    tell = StringField(
        'tell',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 11, "確認してください(-は入れない)")]
    )

    prefecture = StringField(
        'prefecture',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 10, "確認してください(最大10文字)")],
    )

    city = StringField(
        'city',
        [validators.DataRequired("必須項目"),
         validators.Length(-1, 20, "確認してください(最大20文字)")],
    )
    sub = SubmitField("登録")
