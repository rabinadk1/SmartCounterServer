from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Counters(db.Model):
    __tablename__ = "counters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)


class Buses(db.Model):
    __tablename__ = "buses"
    id = db.Column(db.Integer, primary_key=True)
    busnumber = db.Column(db.String, unique=True, nullable=False)
    sourceid = db.Column(db.Integer, db.ForeignKey("counters.id"), nullable=False)
    destinationid = db.Column(db.Integer, db.ForeignKey("counters.id"), nullable=False)
    departuretime = db.Column(db.String, nullable=False)


class CustomerInfo(db.Model):
    __tablename__ = "customerinfo"
    __tableargs__ = (
        CheckConstraint('contact>0')
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact = db.Column(db.BigInteger, nullable=False)
    seats = db.Column(db.ARRAY(db.String, zero_indexes=True), nullable=False)
    busid = db.Column(db.Integer, db.ForeignKey("buses.id"), nullable=False)



class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    counterid = db.Column(db.Integer, db.ForeignKey("counters.id"), nullable=False)

