from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///spotx.db'
app.config['SECRET_KEY']='9397b9b9216e01b685a13fb7'

db=SQLAlchemy(app)



bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'