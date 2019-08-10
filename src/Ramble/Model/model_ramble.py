from src import db

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
    ramble_detail = db.relationship('RambleDetail', lazy='joined')
    point = db.relationship('InterestPoint', secondary='ramble_details', lazy='joined')

class RambleDetail(db.Model):

    __tablename__ = 'ramble_details'
    id = db.Column(db.Integer, primary_key=True)
    ramble_id = db.Column(db.Integer, db.ForeignKey('rambles.id'))
    point_id = db.Column(db.Integer, db.ForeignKey('interest_points.id'))
    ordre = db.Column(db.Integer)
