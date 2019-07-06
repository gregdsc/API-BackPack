from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from Source.Configuration.Session import *
from configuration import *
from Source.Configuration.Database_url import *
from Source.__init__ import *
from sqlalchemy import ForeignKey
from flask import current_app, abort
from Source.Comment.Model.model_comment import *
from Source.Ramble.Model.model_ramble import *
from Source.Point.Model.model_point import *

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    mail = db.Column(db.String(255))
    description = db.Column(db.String(500))
    user_picture = db.relationship('User_picture', lazy='joined')
    comment = db.relationship('Comment', lazy='joined')
    point = db.relationship('Interest_point', lazy='joined')
    ramble = db.relationship('Ramble', lazy='joined')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None, abort(400)
        except BadSignature:
            return None, abort(400)
        user = session.query(User).filter(User.id == data['id']).first()
        return user

class User_picture(db.Model):
    __tablename__ = 'user_pictures'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    url = db.Column(db.String(255))