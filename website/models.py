from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, Integer, String

db = SQLAlchemy()
metadata = MetaData()

# Define the user table with extend_existing=True
user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), unique=True, nullable=False),
    Column('email', String(120), unique=True, nullable=False),
    extend_existing=True
)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')