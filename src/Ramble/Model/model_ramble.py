from sqlalchemy import ForeignKey
from src import db

class Ramble(db.Model):
    __tablename__ = 'rambles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    date_ramble = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer)
    travel_time = db.Column(db.Float)
    step_number = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ramble_detail = db.relationship('RambleDetail', lazy='joined', cascade="all,delete")
    point = db.relationship('InterestPoint', secondary='ramble_details', lazy='joined')
    visible = db.Column(db.Boolean)

class Tag(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class RambleDetail(db.Model):
    __tablename__ = 'ramble_details'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    ramble_id = db.Column(db.Integer, db.ForeignKey('rambles.id'))
    point_id = db.Column(db.Integer, db.ForeignKey('interest_points.id'))
    ordre = db.Column(db.Integer)
