from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings import DB_URI
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from db import session
from flask_cors import CORS
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET_KEY'] = "I7QkQImQ6468QJkKQJ434QHJHFLSssjd"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


comment_poi_association = db.Table(
    'comment_poi',
    db.Column('poi_id', db.Integer, ForeignKey('interestPoint.id')),
    db.Column('comment_id', db.Integer, ForeignKey('comments.id'))
)


user_comment_association = db.Table(
    'user_comment',
    db.Column('comment_id', db.Integer, ForeignKey('comments.id')),
    db.Column('user_id', db.Integer, ForeignKey('users.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    password_hash = db.Column(db.String(255))
    description = db.Column(db.String(500))
    pic_url = db.Column(db.String(255))
    #comment = db.relationship('Comment', lazy='joined')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = session.query(User).filter(User.id == data['id']).first()
        return user


class ImageUrls(db.Model):
    __tablename__ = 'imageUrls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    poiName = db.Column(db.String)


class InterestPoint(db.Model):
    __tablename__ = 'interestPoint'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    userName = db.Column(db.String(255))
    type = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    rank = db.Column(db.Integer)
    comment = db.relationship('Comment', lazy='joined')
    imageUrls = []


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
    username = db.Column(db.String(255))


class Ramble(db.Model):

    _tablename__ = 'ramble'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    userName = db.Column(db.String(255))
    date_ramble = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer)
    travel_time = db.Column(db.Float)
    step_number = db.Column(db.Float)
    ramble_d = db.relationship('Ramble_details', backref='ramble_details', lazy='dynamic')


class Ramble_details(db.Model):

    _tablename__ = 'ramble_details'
    id = db.Column(db.Integer, primary_key=True)
    id_ramble = db.Column(db.Integer, db.ForeignKey('ramble.id'))
    point = db.Column(db.Integer)
    ordre = db.Column(db.Integer)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    creation = db.Column(db.DateTime)
    details = db.Column(db.String(255))
    derniere_modification = db.Column(db.DateTime)
    rank = db.Column(db.Integer)
    point_id = db.Column(db.Integer, db.ForeignKey('interestPoint.id'))


if __name__ == '__main__':
    manager.run()

