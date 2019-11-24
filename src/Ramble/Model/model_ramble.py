from sqlalchemy import ForeignKey
from src import db

RambleTagAssociation = db.Table(
    'ramble_tag_association',
    db.Column('ramble_id', db.Integer, ForeignKey('tags.id')),
    db.Column('tag_id', db.Integer, ForeignKey('rambles.id'))
)

class Ramble(db.Model):
    __tablename__ = 'rambles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    date_ramble = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer)
    travel_time = db.Column(db.Float)
    step_number = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    ramble_detail = db.relationship('RambleDetail', lazy='joined')
    point = db.relationship('InterestPoint', secondary='ramble_details', lazy='joined')
    tag = db.relationship('Tag', secondary='ramble_tag_association')
    visible = db.Column(db.Boolean)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    ramble = db.relationship('Ramble', secondary='ramble_tag_association')

class RambleDetail(db.Model):
    __tablename__ = 'ramble_details'
    id = db.Column(db.Integer, primary_key=True)
    ramble_id = db.Column(db.Integer, db.ForeignKey('rambles.id'))
    point_id = db.Column(db.Integer, db.ForeignKey('interest_points.id'))
    ordre = db.Column(db.Integer)
