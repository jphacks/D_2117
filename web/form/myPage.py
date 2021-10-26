import flask_wtf
from wtforms import SubmitField, HiddenField


class MyPageForm(flask_wtf.FlaskForm):
    pet_id = HiddenField("pet_id")
    lost = SubmitField("迷子")


class MyPageDelForm(flask_wtf.FlaskForm):
    thread_id = HiddenField("thread_id")
    delete = SubmitField("削除")
