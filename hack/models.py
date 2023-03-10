from hack import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view = "login"


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(64),index=True)
    password = db.Column(db.String)
    files = db.relationship('File')
    repos = db.relationship('Repo')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    file = db.Column(db.String, nullable=False)
    uploader = db.Column(db.Integer, db.ForeignKey('user.id'))
    repo = db.Column(db.Integer, db.ForeignKey('repo.id'))

class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_private = db.Column(db.Boolean, default=False)
    files = db.relationship('File')


