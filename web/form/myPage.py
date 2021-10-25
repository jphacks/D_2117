import flask_wtf
from wtforms import SubmitField, HiddenField


class MyPageForm(flask_wtf.FlaskForm):
    pet_id = HiddenField("petid")
    lost = SubmitField("迷子")
