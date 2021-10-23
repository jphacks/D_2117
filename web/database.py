from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import yaml

with open('./web/secret.yaml') as f:
    secret = yaml.safe_load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secret['db']['config']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secret['db']['secret_key']
db = SQLAlchemy(app)
