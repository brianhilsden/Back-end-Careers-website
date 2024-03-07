from flask import Flask
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://avnadmin:AVNS_cVN41Ne4egx4yWk35tZ@mysql-7a9d636-royalty-inc20.a.aivencloud.com:16051/defaultdb'
""" app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newermket.db' """

app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594de3'

CORS(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_message_category="info"

from jobs import routes