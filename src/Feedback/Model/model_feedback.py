from sqlalchemy import ForeignKey
from src import db

user_feedback_association = db.Table(
    'user_feedback',
    db.Column('feedback_id', db.Integer, ForeignKey('feedbacks.id')),
    db.Column('user_id', db.Integer, ForeignKey('users.id'))
)


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    mark = db.Column(db.Integer)
    details = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))