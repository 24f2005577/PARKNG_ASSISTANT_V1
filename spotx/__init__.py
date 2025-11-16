# Import necessary Flask extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_simple_crypt import SimpleCrypt

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI and secret key for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotx.db'
app.config['SECRET_KEY'] = '9397b9b9216e01b685a13fb7'

# Initialize the encryption cipher and attach it to the app
cipher = SimpleCrypt()
cipher.init_app(app)

# Initialize Bcrypt for password hashing
Bcrypt = Bcrypt(app)

# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)

# Initialize LoginManager for user session management
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view endpoint
login_manager.login_message_category = 'info'  # Set the flash message category for login

