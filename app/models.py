from flask_login import UserMixin
from app.factory.database import db


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    cash = db.Column(db.Float, default=10000)


class TransactionHistory(UserMixin, db.Model):

    __tablename__ = 'transations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    symbol = db.Column(db.String(20))
    shares = db.Column(db.Integer)
    price = db.Column(db.Float)
    cost = db.Column(db.Float)
    date_time = db.Column(db.DateTime)
