from community import dataBase, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_user):
    return User.query.get(int(id_user))


class User(dataBase.Model, UserMixin):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    name = dataBase.Column(dataBase.String, nullable=False)
    email = dataBase.Column(dataBase.String, nullable=False, unique=True)
    password = dataBase.Column(dataBase.String, nullable=False)
    profile_picture = dataBase.Column(dataBase.String, nullable=False, default='default.jpg')
    posts = dataBase.relationship('Post', backref='author', lazy=True)
    courses = dataBase.Column(dataBase.String, nullable=False, default='Uninformed')

    def count_posts(self):
        return len(self.posts)


class Post(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    title = dataBase.Column(dataBase.String, nullable=False)
    body = dataBase.Column(dataBase.Text, nullable=False)
    created_at = dataBase.Column(dataBase.DateTime, nullable=False, default=datetime.utcnow)
    id_user = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('user.id'), nullable=False)
