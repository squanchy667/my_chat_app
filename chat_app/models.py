from chat_app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    messages = db.relationship('Message', backref='author', lazy=True)


class Message(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(60), nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def get_all_users():
    li = User.query.order_by(User.username).all()
    li2 = []
    for i in li:
        li2.append(str(i.username))
    return li2

