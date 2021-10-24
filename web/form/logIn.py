import flask_wtf
from wtforms import StringField, SubmitField, validators, IntegerField, PasswordField


class LogInForm(flask_wtf.FlaskForm):

    email = StringField('email',
                        [validators.DataRequired()])

    password = PasswordField(
        'password',
        [validators.DataRequired()]
    )

    sub = SubmitField("登録")
