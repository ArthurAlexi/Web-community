from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

# configurações iniciais do site
app = Flask(__name__)

# app.config['SECRET_KEY'] = '6270739a3c215cd69fff446fa8566fa3'
# if os.getenv("DATABASE_URL"):
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'

app.config['SECRET_KEY'] = '6270739a3c215cd69fff446fa8566fa3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


dataBase = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Passa o nome da função em forma de texto
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from community import models

engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspect = sqlalchemy.inspect(engine)
if not inspect.has_table("user"):
    with app.app_context():
        dataBase.drop_all()
        dataBase.create_all()
        print("Created Database")
else:
    print("database already exists")


from community import routes
