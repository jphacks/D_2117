from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
import yaml
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

with open('./web/secret.yaml') as f:  # 設定ファイル
    secret = yaml.safe_load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secret['db']['config']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = './web/static/images'
app.secret_key = secret['db']['secret_key']
db = SQLAlchemy(app)


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)  # 通し番号
    user_nickname = db.Column(db.String(10), nullable=False)  # ニックネーム
    user_fname = db.Column(db.String(10), nullable=False)  # 名前
    user_lname = db.Column(db.String(10), nullable=False)  # 苗字
    email = db.Column(db.String(50), unique=True, nullable=False)  # メール
    tell = db.Column(db.String(12),  unique=True, nullable=False)  # 電話
    prefecture = db.Column(db.String(10), nullable=False)  # 県
    city = db.Column(db.String(20), nullable=False)  # 市
    point = db.Column(db.Integer, default=1000)  # アプリ内通貨
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 変更日時

    def __init__(self, user_nickname, user_fname, user_lname, email, tell, prefecture, city):
        self.user_nickname = user_nickname
        self.user_fname = user_fname
        self.user_lname = user_lname
        self.email = email
        self.tell = tell
        self.prefecture = prefecture
        self.city = city

    def update(self, user_nickname, user_fname, user_lname, tell, prefecture, city):
        self.user_nickname = user_nickname
        self.user_fname = user_fname
        self.user_lname = user_lname
        self.tell = tell
        self.prefecture = prefecture
        self.city = city


class UserLogin(db.Model):
    email = db.Column(db.String(50), primary_key=True)  # メール
    last_login = db.Column(db.DateTime)  # 最終ログイン時刻
    password_hash = db.Column(db.String(1000), nullable=False)  # ハッシュ化したパスワード
    email_check = db.Column(db.String(300))  # メール確認用の文字列(認証済みなら"")

    def __init__(self, email, password, email_check):
        self.email = email
        self.password_hash = generate_password_hash(password)  # パスワードをハッシュ化
        self.email_check = email_check

    # 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def login(self):
        self.last_login = datetime.datetime.now()


class Pet(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True,
                       autoincrement=True)  # 通し番号
    user_id = db.Column(db.Integer, nullable=False)  # 飼い主ID
    pet_name = db.Column(db.String(20), nullable=False)  # ペットの名前
    features_description = db.Column(db.String(500))  # ペットの詳細
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 変更日時
    lost_flag = db.Column(db.Boolean, default=False)  # 行方不明フラグ
    lost_time = db.Column(db.DateTime)  # 行方不明になった時刻

    def __init__(self, user_id, pet_name, features_description):
        self.user_id = user_id
        self.pet_name = pet_name
        self.features_description = features_description

    def lost(self):
        self.lost_flag = True
        self.lost_time = datetime.datetime.now()


class SearchPet(db.Model):
    search_pet_id = db.Column(db.Integer, primary_key=True,
                              autoincrement=True)  # 通し番号
    prefecture = db.Column(db.String(10), nullable=False)  # 県
    city = db.Column(db.String(20), nullable=False)  # 市
    features_description = db.Column(db.String(500))  # ペットの詳細
    img_source = db.Column(db.String(100), nullable=False)  # 画像パス
    found_flag = db.Column(db.Boolean, default=False)  # 発見フラグ
    found_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 登録日時
    email = db.Column(db.String(50), primary_key=True)  # 発見した人のメールアドレス

    def __init__(self, prefecture, city, features_description, img_source):
        self.prefecture = prefecture
        self.city = city
        self.features_description = features_description
        self.img_source = img_source


class Thread(db.Model):
    thread_id = db.Column(db.Integer, primary_key=True,
                          autoincrement=True)  # 通し番号
    user_id = db.Column(db.Integer, nullable=False)  # 飼い主ID
    pet_id = db.Column(db.Integer)  # ペットのID
    reply_id = db.Column(db.Integer, default=0, nullable=False)  # リプライID
    img_source = db.Column(db.String(100), default=None)  # 画像パス
    message = db.Column(db.String(500))  # メッセージ
    lost_flag = db.Column(db.Boolean, default=False)
    del_flag = db.Column(db.Boolean, default=False)  # 削除フラグ
    total_point = db.Column(db.Integer, default=0)  # スレッド内の総移動数
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時

    def __init__(self, user_id, pet_id, reply_id, img_source, message, lost_flag=False):
        self.user_id = user_id
        self.pet_id = pet_id
        self.reply_id = reply_id
        self.img_source = img_source
        self.message = message
        self.lost_flag = lost_flag


db.create_all()
if User.query.first() is None:
    new_user = User("管理者", "01", "管理者",
                    secret['db']['user'], "00000000000", "長野県", "茅野市")
    new_user_pass = UserLogin(secret['db']['user'], secret['db']['pass'], None)
    try:
        db.session.add(new_user)
        db.session.add(new_user_pass)
        db.session.commit()
    except:
        raise "管理者の作成に失敗"
