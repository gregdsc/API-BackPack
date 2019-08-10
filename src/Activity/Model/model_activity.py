from src import db


class Activity(db.Model):
    _tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.String(255))
    pas = db.Column(db.Integer)
    km = db.Column(db.Float)
    calorie = db.Column(db.Float)
    speed = db.Column(db.Float)
    type = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
