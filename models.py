from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(150), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logout_timestamp = db.Column(db.DateTime(), nullable=True)
    login_timestamp = db.Column(db.DateTime(), nullable=True)
    


class Song(db.Model):
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    artist = db.Column(db.String(150), nullable=True)    


