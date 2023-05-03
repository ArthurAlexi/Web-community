from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# configurações iniciais do site
app = Flask(__name__)

app.config['SECRET_KEY'] = '6270739a3c215cd69fff446fa8566fa3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'

dataBase = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Passa o nome da função em forma de texto
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from community import routes
