from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Counters(db.Model):
    __tablename__ = "counters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    counterid = db.Column(db.Integer, db.ForeignKey("counters.id"), nullable=False)
