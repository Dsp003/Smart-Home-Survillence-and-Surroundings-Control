from flask import Flask
# from flask_ngrok import run_with_ngrok
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '0a05c113e413852b7b25915a96ffca9a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# run_with_ngrok(app)

from stream import routes
