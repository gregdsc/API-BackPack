from Source.__init__ import *
from Source.User.Model.model_user import *

class Interest_point(db.Model):
    __tablename__ = 'interest_points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    username = db.Column(db.String(255))
    type = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    rank = db.Column(db.Integer)
    comment = db.relationship('Comment', lazy='joined')
    point_picture = db.relationship('Point_picture', lazy='joined')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ramble = db.relationship('Ramble', secondary='ramble_details')

class Point_picture(db.Model):
    __tablename__ = 'point_pictures'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    point_id = db.Column(db.Integer, ForeignKey('interest_points.id'))
