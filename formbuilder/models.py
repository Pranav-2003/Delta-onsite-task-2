from datetime import datetime
from formbuilder import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Questions(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(10),nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    data = db.Column(db.String(120), nullable=False)
    reply = db.relationship('Replies', backref='question', lazy=True)
    
class Replies(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    qid = db.Column(db.Integer, db.ForeignKey('questions.sno'), nullable=False)
    data = db.Column(db.String(70), nullable=False)
    
class Formtitles(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    uid = db.Column(db.Integer, nullable=False)


    