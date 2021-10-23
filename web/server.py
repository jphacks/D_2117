from web.database import *
from waitress import serve
from flask import render_template, request, redirect
from web.form import *


"""ログイン関連"""

login_manager = flask_login.LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])  # ログイン
def login():
    if flask_login.current_user.is_authenticated:  # すでにログイン中なら/に飛ばす
        return redirect("/")

    form = LogInForm(request.form)
    if form.validate_on_submit():
        userlogin = UserLogin.query.filter_by(
            email=form.email.data).one_or_none()

        userlogin.login()  # ログイン時刻を記録
        try:
            db.session.add(userlogin)  # 最終ログイン時刻の記録
            db.session.commit()
        except:
            pass

        user = User.query.filter_by(email=form.email.data).one_or_none()
        flask_login.login_user(user)  # flaskloginにログイン中のユーザに登録

        return redirect("/")  # ログインに成功したらトップページへ移動

    return render_template("login.html", form=form)


"""webページ"""


@app.route("/", methods=["GET"])  # トップページ
def thread():
    return render_template("thread.html")


@app.route("/test", methods=["GET"])  # Debug
def test():
    return render_template("common.html")


@app.route("/memberInfo", methods=["GET", "POST"])  # 新規会員情報入力ページ
def memberInfo():
    form = MemberInfoForm(request.form)
    if form.validate_on_submit():
        new_user = User(form.user_nickname.data, form.user_fname.data, form.user_lname.data,
                        form.email.data, form.tell.data, form.prefecture.data, form.city.data)
        new_user_pass = UserLogin(form.email.data, "password")
        try:
            db.session.add(new_user)
            db.session.add(new_user_pass)
            db.session.commit()
        except:
            print("登録失敗")
    return render_template("memberInfo.html", form=form)


@app.route("/searchPet", methods=["GET", "POST"])  # ペット探し
def searchPet():
    form = SearchPetForm(request.form)
    if form.validate_on_submit():
        new_searchpet = SearchPet(form.features_description.data, form.prefecture.data, form.city.data,
                                  form.img.data)
        try:
            db.session.add(new_searchpet)
            db.session.commit()
        except:
            print("登録失敗")
    return render_template("searchPet.html", form=form)

# ログインしてからのページ


@app.route("/threadDetail", methods=["GET"])  # スレッド詳細ページ
@flask_login.login_required
def threadDetail():
    return render_template("threadDetail.html")


@app.route("/myPage", methods=["GET"])  # マイページ
@flask_login.login_required
def myPage():
    return render_template("myPage.html")


@app.route("/memberInfoFix", methods=["GET"])  # 会員情報修正ページ
@flask_login.login_required
def memberInfoFix():
    return render_template("memberInfoFix.html")


"""AI関連テスト"""


@app.route("/ai", methods=["GET"])
def ai():
    return "AIテスト"


"""サーバの起動"""


def main():
    app.run(host='0.0.0.0', port=7777, debug=True)
    # serve(app, host='0.0.0.0', port=5000)
