from flask import render_template, request, redirect, flash, send_from_directory
import flask_login
from waitress import serve
from web.form import *
from web.database import *
from werkzeug.utils import secure_filename
import requests
import os
import glob
import numpy as np


"""完了済み"""

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

        if userlogin is None or not userlogin.check_password(form.password.data):
            return "ログインに失敗"

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


@app.route("/logout", methods=['GET'])  # ログアウトページ
@ flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.route("/redirect", methods=['GET'])  # リダイレクト時に表示するページ
def app_redirect():
    return render_template("redirect.html", status=request.args.get("status"), next=request.args.get("next"))


@app.route("/memberInfo", methods=["GET", "POST"])  # 新規会員情報入力ページ
def memberInfo():
    form = MemberInfoForm(request.form)
    if form.validate_on_submit():
        new_user = User(form.user_nickname.data, form.user_fname.data, form.user_lname.data,
                        form.email.data, form.tell.data, form.prefecture.data, form.city.data)
        new_user_pass = UserLogin(form.email.data, form.password.data)
        try:
            db.session.add(new_user)
            db.session.add(new_user_pass)
            db.session.commit()
        except:
            return "登録失敗"

        return redirect("/login")
    return render_template("memberInfo.html", form=form)


@app.route("/petInfo", methods=["GET", "POST"])  # ペットの登録
@ flask_login.login_required
def petInfo():
    form = PetInfoForm(request.form)
    if form.validate_on_submit():
        new_pet = Pet(flask_login.current_user.id,
                      form.pet_name.data, form.features_description.data)
        try:
            db.session.add(new_pet)
            db.session.commit()
        except:
            return "登録失敗"
        return redirect("/myPage")
    return render_template("petInfo.html", form=form)


def ai_api(img_path):  # ベクトルの計算
    """
    # api_keyが正しい場合
    -> {'authentication': 'ok', 'vector': [-1.6974670886993408, -1.3484156131744385, ..., -0.9846966862678528]}
    # api_keyが間違っている場合
    -> {'authentication': 'no'}
    """
    endpoint = "http://127.0.0.1:7775/predict"
    with open('web/secret.yaml', 'r') as f:
        secret = yaml.safe_load(f)
    api_key = secret['AI']['API_KEY']

    try:
        resp = requests.post(endpoint, files={"file": open(
            os.path.join(app.config['UPLOAD_FOLDER'], img_path), 'rb')}, headers={'api_key': api_key})
    except:
        print("ベクトル変換でエラーが発生しています")
        return None

    resp_dict = resp.json()
    if resp_dict["authentication"] == 'ok':
        return resp_dict["vector"]  # 4096次元ベクトルがlist型で格納される
    else:
        print("ベクトル変換エラー")
        return None


def get_cos_sim(v1, v2):
    """
    画像から出力した2つのベクトルからコサイン類似度を計算するメソッド

    Parameters
    ----------
    v1 : list or numpy
        1つめのベクトル
    v2 : list or numpy
        2つめのベクトル
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def predict_pet(vector1, lostpetlist):  # 発見されたペットのベクトル, 迷子の犬の一覧
    max_ans = 2
    ans = np.zeros((max_ans, 2))
    for pet_id in lostpetlist:
        for npy in glob.glob("./web/static/vector/"+str(pet_id)+"/*"):
            vector2 = np.load(npy)
            sim = get_cos_sim(vector1, vector2)  # ベクトルの類似度計算
            if sim > ans[0, 1]:  # 計算した類似度が上位項目より大きければ
                npindex = np.where(ans[:, 0] == pet_id)
                if npindex[0].size != 0:  # すでにpet_idがあれば
                    if sim > ans[npindex[0], 1]:  # 新しい方が大きければ更新
                        ans[npindex] = (pet_id, sim)
                else:
                    ans[0] = (pet_id, sim)
            ans = ans[np.argsort(ans[:, 1])]  # 類似度を昇順にソート
    return ans[:, 0][::-1]


@app.route("/searchPet", methods=["GET", "POST"])  # ペット探し
def searchPet():
    form = SearchPetForm(request.form)
    if form.validate_on_submit():
        # 画像を加工・保存
        img = request.files['img']
        filename = secure_filename(img.filename)
        if filename == '':
            return "画像を登録してください"
        filename = "".join(filename.split(".")[:-1])  # 拡張子を削除
        img_url = os.path.join('search', filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_url+".jpg"))

        # AI関連の記述する部分
        try:
            vector = np.array(ai_api(img_url+".jpg"))
        except:
            return redirect("/searchPet")
        lostpetlist = [pet.pet_id for pet in Pet.query.filter_by(
            lost_flag=True).all()]

        for pet_id in predict_pet(vector, lostpetlist):
            predict_thread = Thread.query.filter_by(
                pet_id=pet_id, img_source="common/C1").first()

        del img  # メモリ対策
        new_searchpet = SearchPet(
            form.prefecture.data, form.city.data, form.features_description.data, img_url)
        try:
            db.session.add(new_searchpet)
            db.session.commit()
        except:
            return "登録失敗"
        return redirect("/")

    return render_template("searchPet.html", form=form)


@ app.route("/", methods=["GET", "POST"])
@ app.route("/thread/<reply_id>", methods=["GET", "POST"])  # トップページ(スレッド一覧)
def thread(reply_id="0"):
    if reply_id.isdigit() == False:
        reply_id = 0
    if int(reply_id) < 0:
        reply_id = 0
    reply_id = int(reply_id)

    threadtop = Thread.query.filter_by(
        thread_id=reply_id, del_flag=False).first()
    threadlist = Thread.query.filter_by(reply_id=reply_id, del_flag=False)
    nicknamelist = User.query.with_entities(User.id, User.user_nickname)

    if reply_id == 0:
        threadlist = threadlist.order_by(Thread.thread_id.desc()).all()
    elif threadtop is None or threadtop.img_source == "":
        return redirect("/")
    else:
        threadlist = threadlist.order_by(Thread.thread_id).all()

    # スレッドの作成にはログイン、ペットの登録がいる
    # 返信にはログインがいる

    form = ThreadForm(request.form)

    if flask_login.current_user.is_authenticated:

        pet_list = Pet.query.filter_by(
            user_id=flask_login.current_user.id).all()
        if len(pet_list) > 0:
            # ペットの名前をセレクトできるように
            form.pet_id.choices = [(pet.pet_id, pet.pet_name)
                                   for pet in pet_list]
        if form.is_submitted():
            # 画像を加工・保存
            if 'img' in request.files:
                img = request.files['img']
                filename = secure_filename(img.filename)

                if filename == '' and reply_id == 0:
                    return "画像を登録してください"

                if reply_id == 0:  # トップページのスレッドは必ず写真あり
                    filename = "".join(filename.split(".")[:-1])  # 拡張子を削除
                    img_url = os.path.join(form.pet_id.data, filename)
                    os.makedirs(os.path.join(
                        app.config['UPLOAD_FOLDER'], form.pet_id.data), exist_ok=True)
                    img.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], img_url+".jpg"))

                    try:
                        # AI関連の記述する部分
                        vector = np.array(ai_api(img_url+".jpg"))
                        vector_url = os.path.join(
                            './web/static/vector/', img_url)
                        os.makedirs(os.path.join("./web/static/vector/",
                                    form.pet_id.data), exist_ok=True)
                        np.save(vector_url, vector)
                    except:
                        pass

                    del img  # メモリ対策
            else:
                img_url = None

            # DBへ保存
            new_thread = Thread(flask_login.current_user.id,
                                form.pet_id.data, reply_id, img_url, form.message.data)
            try:
                db.session.add(new_thread)
                db.session.commit()
            except:
                return "登録失敗"
            return redirect("/redirect?status=threadsuccess&next="+str(reply_id))
    return render_template("thread.html", form=form, reply_id=reply_id, threadlist=threadlist, threadtop=threadtop, nicknamelist=nicknamelist)


"""開発中"""


@ app.route("/myPage", methods=["GET", "POST"])  # マイページ
@ flask_login.login_required
def myPage():
    form = MyPageForm(request.form)
    delform = MyPageDelForm(request.form)
    if form.validate_on_submit() and form.pet_id.data:
        update_pet = Pet.query.filter_by(pet_id=form.pet_id.data).first()
        update_pet.lost()  # 迷子申請があったら迷子登録

        # 迷子捜索用のスレッド
        message = "名前："+update_pet.pet_name+"\n特徴：\n"+update_pet.features_description + \
            "\n迷子登録された時刻：" + \
            update_pet.lost_time.strftime(
                "%y/%m/%d %H:%M")+"\n\n下の返信より情報提供お願いします。"
        lost_thread = Thread(flask_login.current_user.id,
                             form.pet_id.data, 0, "common/C1", message)

        try:
            db.session.add(update_pet)
            db.session.add(lost_thread)
            db.session.commit()
        except:
            return "登録失敗"
    elif delform.validate_on_submit() and delform.thread_id.data:
        del_thread = Thread.query.filter_by(
            thread_id=delform.thread_id.data).first()
        del_thread.del_flag = True
        try:
            db.session.add(del_thread)
            db.session.commit()
        except:
            return "削除に失敗"
    pet_list = Pet.query.filter_by(
        user_id=flask_login.current_user.id).all()
    threadlist = Thread.query.filter_by(
        user_id=flask_login.current_user.id, del_flag=False).order_by(Thread.thread_id.desc()).all()
    lostthread = Thread.query.filter_by(img_source="common/C1", del_flag=False)
    return render_template("/myPage.html", form=form, delform=delform, pet_list=pet_list, threadlist=threadlist, lostthread=lostthread)


"""未完成"""


@ app.route("/memberInfoFix", methods=["GET"])  # 会員情報修正ページ
@ flask_login.login_required
def memberInfoFix():
    return render_template("memberInfoFix.html")


"""サーバの起動"""


def main():
    app.run(host='0.0.0.0', port=7777, debug=True)
    # serve(app, host='0.0.0.0', port=7777)
