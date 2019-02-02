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
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    counter = db.Column(db.Integer, db.ForeignKey("counters.id"), nullable=False)
