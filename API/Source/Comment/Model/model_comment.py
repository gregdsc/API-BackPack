from Source.User.Model.model_user import *


comment_poi_association = db.Table(
    'comment_poi',
    db.Column('poi_id', db.Integer, ForeignKey('interest_points.id')),
    db.Column('comment_id', db.Integer, ForeignKey('comments.id'))
)


user_comment_association = db.Table(
    'user_comment',
    db.Column('comment_id', db.Integer, ForeignKey('comments.id')),
    db.Column('user_id', db.Integer, ForeignKey('users.id'))
)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    creation = db.Column(db.DateTime)
    details = db.Column(db.String(255))
    derniere_modification = db.Column(db.DateTime)
    rank = db.Column(db.Integer)
    point_id = db.Column(db.Integer, db.ForeignKey('interest_points.id'))