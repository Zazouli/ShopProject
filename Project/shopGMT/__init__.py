from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

appshop = Flask(__name__)
appshop.config["SECRET_KEY"] = 'edd0e454302ebb2bc4dedbebec613c10'
appshop.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'

db = SQLAlchemy(appshop)
bcrypt=Bcrypt(appshop)
login_manager=LoginManager(appshop)
from shopGMT import route
