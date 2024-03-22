from app import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Diameter(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Double, nullable=False)
    # One-to-many relationship: a Diameter can have multiple Sessions
    sessions = relationship('Session', backref='diameter')

class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('diameter.device_id'))
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=True)  # in seconds
    distance = db.Column(db.Double, nullable=True)
    speed = db.Column(db.Double, nullable=True)
    # One-to-many relationship: a Session can have multiple Records
    records = relationship('Record', backref='session')

class Record(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    sensor_triggers = db.Column(db.Integer, nullable=True)
