from web.database import *
from waitress import serve
from flask import render_template, request, redirect


"""ログイン関連"""

login_manager = flask_login.LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])  # ログイン
def login():
    return render_template("login.html")


"""webページ"""


@app.route("/", methods=["GET"])  # トップページ
def thread():
    return render_template("thread.html")


@app.route("/test", methods=["GET"])  # Debug
def test():
    return render_template("common.html")


@app.route("/memberInfo", methods=["GET", "POST"])  # 新規会員情報入力ページ
def memberInfo():
    return render_template("memberInfo.html")


@app.route("/searchPet", methods=["GET", "POST"])  # ペット探し
def searchPet():
    return render_template("searchPet.html")

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


"""サーバの起動"""


def main():
    app.run(host='0.0.0.0', port=7777, debug=True)
    # serve(app, host='0.0.0.0', port=5000) # 本番用のサーバ
